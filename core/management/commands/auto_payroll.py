import datetime
from django.core.management.base import BaseCommand
from core.models import Employee, Payroll, Loan, Payroll_Deduction, Loan_Payment, Payslip

class Command(BaseCommand):
    help = 'Automatically generates payroll for all active employees for the current month.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting automated payroll generation...")
        
        active_employees = Employee.objects.filter(status='Active')
        now = datetime.datetime.now()
        month_name = now.strftime("%B")
        year = now.year
        
        count = 0
        skipped_count = 0
        
        for emp in active_employees:
            # Check if payroll already generated for this month
            if Payroll.objects.filter(employee=emp, month=month_name, year=year).exists():
                skipped_count += 1
                continue
            
            basic = emp.designation.basic_salary
            
            # Create Payroll Entry
            payroll = Payroll.objects.create(
                employee=emp,
                month=month_name,
                year=year,
                basic_salary=basic,
                total_allowances=0,
                total_deductions=0,
                net_salary=basic
            )
            
            # Handle Loan Deductions
            active_loans = Loan.objects.filter(employee=emp, status='Active')
            total_loan_deduction = 0
            
            for loan in active_loans:
                deduction_amount = loan.monthly_repayment
                if deduction_amount > 0:
                    # Create Deduction Record
                    Payroll_Deduction.objects.create(
                        payroll=payroll,
                        name=f"Loan Repayment (ID: {loan.loan_id})",
                        amount=deduction_amount
                    )
                    
                    # Record the Loan Payment transaction
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
            
            # Generate dummy Payslip reference
            Payslip.objects.create(
                payroll=payroll,
                pdf_path=f"/payslip/{payroll.payroll_id}/" 
            )
            count += 1
            
        self.stdout.write(self.style.SUCCESS(f'Automated Payroll Complete: Generated {count} payrolls. Skipped {skipped_count}.'))
