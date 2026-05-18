import datetime
import time

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Sum
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, EmployeeForm, DepartmentForm, DesignationForm, AttendanceForm, LoanForm, PayrollAllowanceForm, PayrollDeductionForm, PayrollEditForm
from .models import User, Employee, Department, Designation, Attendance, Payroll, Loan, Payslip, Payroll_Allowance, Payroll_Deduction, Loan_Payment

# ── Public Home Page ──────────────────────────────────────
def home_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard')
        return redirect('employee_dashboard')
    return render(request, 'core/home.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('dashboard')
            else:
                return redirect('employee_dashboard')

    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    if not request.user.is_staff:
        return redirect('employee_dashboard')
        
    # Stats for dashboard

    total_employees = Employee.objects.count()
    active_employees = Employee.objects.filter(status='Active').count()
    departments_count = Department.objects.count()
    designations_count = Designation.objects.count()
    
    # Recent 5 employees
    recent_employees = Employee.objects.order_by('-date_of_joining')[:5]
    
    # Dynamic Growth Calculation (Last 30 days vs Previous 30 days)
    now = timezone.now()
    thirty_days_ago = now - datetime.timedelta(days=30)
    sixty_days_ago = now - datetime.timedelta(days=60)
    
    recent_joins = Employee.objects.filter(date_of_joining__gte=thirty_days_ago.date()).count()
    previous_joins = Employee.objects.filter(date_of_joining__gte=sixty_days_ago.date(), date_of_joining__lt=thirty_days_ago.date()).count()
    
    if previous_joins > 0:
        emp_growth = int((recent_joins / previous_joins) * 100)
    else:
        emp_growth = 100 if recent_joins > 0 else 0
        
    # Get total payroll expense for this month to use as a dynamic metric
    curr_month = now.strftime("%B")
    curr_year = now.year
    total_payroll_expense_raw = Payroll.objects.filter(month=curr_month, year=curr_year).aggregate(Sum('net_salary'))['net_salary__sum'] or 0

    # Format it compactly (e.g. 35200 -> 35.2K)
    def format_currency(num):
        num = float(num)
        if num >= 1000000:
            return f"{num / 1000000:.1f}M".rstrip('0').rstrip('.')
        elif num >= 1000:
            return f"{num / 1000:.1f}K".replace('.0K', 'K')
        return str(int(num))
        
    total_payroll_expense = format_currency(total_payroll_expense_raw)

    
    # Active Loans count
    active_loans_count = Loan.objects.filter(status='Active').count()

    # Data for Charts
    # 1. Department Distribution
    dept_data = Employee.objects.values('department__name').annotate(count=Count('employee_id'))
    dept_labels = [item['department__name'] for item in dept_data]
    dept_counts = [item['count'] for item in dept_data]
    
    # 2. System Uptime (Dynamic Simulation based on server start time)
    server_start_time = int(time.time()) - (2 * 3600 + 15 * 60) # Simulated 2h 15m uptime
    
    # 3. Payroll Expense (Last 6 months)
    all_payrolls = Payroll.objects.all().values('month', 'year', 'net_salary')
    # Simple aggregation in python
    payroll_map = {} # Key: "Month Year", Value: total
    for p in all_payrolls:
        key = f"{p['month']} {p['year']}"
        payroll_map[key] = payroll_map.get(key, 0) + float(p['net_salary'])
    
    # Sort roughly? In a real app we'd sort by date. 
    # Let's take the keys and values.
    payroll_labels = list(payroll_map.keys())
    payroll_values = list(payroll_map.values())
    
    context = {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'departments_count': departments_count,
        'designations_count': designations_count,
        'recent_employees': recent_employees,
        'active_loans_count': active_loans_count,
        'dept_labels': dept_labels,
        'dept_counts': dept_counts,
        'payroll_labels': payroll_labels,
        'payroll_values': payroll_values,
        'emp_growth': emp_growth,
        'total_payroll_expense': total_payroll_expense,
        'server_start_time': server_start_time,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'core/employee_list.html', {'employees': employees})

@login_required
def employee_add(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            # Extract user data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken. Please choose a different username.')
                return render(request, 'core/employee_form.html', {'form': form, 'title': 'Add Employee'})

            # Create User and Employee atomically
            try:
                user = User.objects.create_user(username=username, password=password)
                employee = form.save(commit=False)
                employee.user = user
                employee.save()
                messages.success(request, 'Employee added successfully.')
                return redirect('employee_list')
            except Exception as e:
                # Clean up orphan user if employee save failed
                if 'user' in locals() and user.pk:
                    user.delete()
                messages.error(request, f'Error creating employee: {e}')
    else:
        form = EmployeeForm()
    return render(request, 'core/employee_form.html', {'form': form, 'title': 'Add Employee'})

@login_required
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        # Note: Editing username/password/role might need separate handling or just ignore here if not intended
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully.')
            return redirect('employee_list')
    else:
        # Pre-populate role/username if needed, but for now just employee data
        form = EmployeeForm(instance=employee)
    return render(request, 'core/employee_form.html', {'form': form, 'title': 'Edit Employee'})

@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        user = employee.user
        employee.delete()
        user.delete() # Delete associated user
        messages.success(request, 'Employee deleted.')
        return redirect('employee_list')
    return render(request, 'core/employee_confirm_delete.html', {'employee': employee})

@login_required
def department_list(request):
    departments = Department.objects.all()
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department added.')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'core/department_list.html', {'departments': departments, 'form': form})

@login_required
def designation_list(request):
    designations = Designation.objects.all()
    if request.method == 'POST':
        form = DesignationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Designation added.')
            return redirect('designation_list')
    else:
        form = DesignationForm()
    return render(request, 'core/designation_list.html', {'designations': designations, 'form': form})

@login_required
def attendance_list(request):
    attendance_records = Attendance.objects.all().order_by('-date')
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance recorded.')
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'core/attendance_list.html', {'attendance_records': attendance_records, 'form': form})

@login_required
def payroll_list(request):
    payrolls = Payroll.objects.all().order_by('-year', '-month')
    return render(request, 'core/payroll_list.html', {'payrolls': payrolls})

@login_required
def payroll_generate(request):
    # Simplified Logic: Create a dummy payroll for all active employees for current month
    # In real app, this would be complex
    active_employees_list = Employee.objects.filter(status='Active')

    if request.method == 'POST':
        employee_id_input = request.POST.get('employee_id')
        if employee_id_input and employee_id_input != 'all':
             employees = Employee.objects.filter(employee_id=employee_id_input, status='Active')
        else:
             employees = Employee.objects.filter(status='Active')

        count = 0
        if 'month' in request.POST and 'year' in request.POST:
            month_name = request.POST.get('month')
            try:
                year = int(request.POST.get('year'))
            except ValueError:
                messages.error(request, "Invalid year format.")
                return redirect('payroll_generate')
        else:
            # Fallback to current date if not provided (though form requires it)
            now_dt = datetime.datetime.now()
            month_name = now_dt.strftime("%B")
            year = now_dt.year

        now = datetime.datetime.now() # Keep for generation date tracking
        
        skipped_count = 0
        
        for emp in employees:
            if Payroll.objects.filter(employee=emp, month=month_name, year=year).exists():
                skipped_count += 1
                continue
            else:
                basic = emp.designation.basic_salary
                
                # Create Payroll first
                payroll = Payroll.objects.create(
                    employee=emp,
                    month=month_name,
                    year=year,
                    basic_salary=basic,
                    total_allowances=0,
                    total_deductions=0,
                    net_salary=basic
                )

                # Loan Logic: Deduct defined monthly repayment
                active_loans = Loan.objects.filter(employee=emp, status='Active')
                total_loan_deduction = 0
                for loan in active_loans:
                    deduction_amount = loan.monthly_repayment
                    
                    # Logic: If remaining loan balance (not tracked perfectly here but for simplicity)
                    # We assume repayment continues until closed manually or we could track balance.
                    # For now, just deduct the set amount.
                    
                    if deduction_amount > 0:
                        # Create Deduction
                        Payroll_Deduction.objects.create(
                            payroll=payroll,
                            name=f"Loan Repayment (ID: {loan.loan_id})",
                            amount=deduction_amount
                        )
                        
                        # Record Loan Payment
                        Loan_Payment.objects.create(
                            loan=loan,
                            employee=emp,
                            payment_date=now,
                            amount=deduction_amount
                        )
                        
                        total_loan_deduction += float(deduction_amount)

                # Update Payroll Totals
                payroll.total_deductions = total_loan_deduction
                payroll.net_salary = float(basic) - total_loan_deduction
                payroll.save()

                # Generate Payslip entry
                Payslip.objects.create(
                    payroll=payroll,
                    pdf_path=f"/payslip/{payroll.payroll_id}/" 
                )
                count += 1
        
        msg = f'Generated payroll for {count} employees.'
        if skipped_count > 0:
            msg += f' Skipped {skipped_count} employees (Payroll already generated for this month). Delete existing payroll records if you wish to regenerate.'
        messages.success(request, msg)
        return redirect('payroll_list')
    return render(request, 'core/payroll_generate.html', {'active_employees': active_employees_list})

@login_required
def allowance_list(request):
    allowances = Payroll_Allowance.objects.all().order_by('-payroll__generated_date')
    if request.method == 'POST':
        form = PayrollAllowanceForm(request.POST)
        if form.is_valid():
            allowance = form.save()
            # Update Payroll Totals
            payroll = allowance.payroll
            payroll.total_allowances += allowance.amount
            payroll.net_salary += allowance.amount
            payroll.save()
            messages.success(request, 'Allowance added.')
            return redirect('allowance_list')
    else:
        form = PayrollAllowanceForm()
    return render(request, 'core/allowance_list.html', {'allowances': allowances, 'form': form})

@login_required
def deduction_list(request):
    deductions = Payroll_Deduction.objects.all().order_by('-payroll__generated_date')
    if request.method == 'POST':
        form = PayrollDeductionForm(request.POST)
        if form.is_valid():
            deduction = form.save()
            # Update Payroll Totals
            payroll = deduction.payroll
            payroll.total_deductions += deduction.amount
            payroll.net_salary -= deduction.amount
            payroll.save()
            messages.success(request, 'Deduction added.')
            return redirect('deduction_list')
    else:
        form = PayrollDeductionForm()
    return render(request, 'core/deduction_list.html', {'deductions': deductions, 'form': form})

@login_required
def payroll_edit(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    if request.method == 'POST':
        form = PayrollEditForm(request.POST, instance=payroll)
        if form.is_valid():
            updated = form.save(commit=False)
            # Auto-calculate net salary from components
            updated.net_salary = updated.basic_salary + updated.total_allowances - updated.total_deductions
            updated.save()
            messages.success(request, 'Payroll has been manually updated.')
            return redirect('payroll_list')
    else:
        form = PayrollEditForm(instance=payroll)
        
    context = {
        'form': form,
        'payroll': payroll,
        'employee': payroll.employee
    }
    return render(request, 'core/payroll_edit.html', context)

@login_required
def payslip_view(request, payroll_id):
    payroll = get_object_or_404(Payroll, payroll_id=payroll_id)
    return render(request, 'core/payslip.html', {'payroll': payroll})

@login_required
def employee_dashboard(request):
    if request.user.is_staff:
        return redirect('dashboard')
    
    # Get employee object linked to user
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        messages.error(request, "No employee profile found for your account.")
        return redirect('login') # Or some error page

    return render(request, 'core/employee_dashboard.html', {'employee': employee})

@login_required
def employee_profile(request):
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return redirect('employee_dashboard')
        
    return render(request, 'core/employee_profile.html', {'employee': employee})

@login_required
def employee_salary(request):
    try:
        employee = Employee.objects.get(user=request.user)
        payrolls = Payroll.objects.filter(employee=employee).order_by('-year', '-month')
    except Employee.DoesNotExist:
        payrolls = []
        
    return render(request, 'core/employee_salary.html', {'payrolls': payrolls})


@login_required
def loan_list(request):
    loans = Loan.objects.all()
    
    # Calculate paid amount for each loan
    for loan in loans:
        total_paid = 0
        payments = Loan_Payment.objects.filter(loan=loan)
        for payment in payments:
            total_paid += payment.amount
        loan.total_paid = total_paid
        loan.balance = loan.loan_amount - total_paid

    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loan application submitted.')
            return redirect('loan_list')
    else:
        form = LoanForm()
    return render(request, 'core/loan_list.html', {'loans': loans, 'form': form})

@login_required
def loan_payment_list(request):
    payments = Loan_Payment.objects.all().order_by('-payment_date')
    return render(request, 'core/loan_payment_list.html', {'payments': payments})

@login_required
def salary_list(request):
    payrolls = Payroll.objects.all().order_by('-generated_date')
    return render(request, 'core/salary_list.html', {'payrolls': payrolls})
