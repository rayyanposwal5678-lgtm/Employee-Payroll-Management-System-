from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from .models import Employee, Department, Designation, Attendance, Loan, Payroll, Payroll_Allowance, Payroll_Deduction

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'new-password', 'placeholder': 'Password'})


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['title', 'basic_salary']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'basic_salary': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(DesignationForm, self).__init__(*args, **kwargs)

class EmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['department'].empty_label = "Select Department"
        self.fields['designation'].empty_label = "Select Designation"
        self.fields['status'].empty_label = "Select Status" # Though this is ChoiceField, empty_label logic is different for standard ChoiceFields but we can use initial or widget placeholder if needed.
        # Actually for standard ChoiceField with a default, it usually selects the default. 
        # But for ModelChoiceField (ForeignKeys), empty_label works.

    # User creation fields
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}))


    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'date_of_joining', 'department', 'designation', 'status']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_of_joining': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'designation': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_date_of_joining(self):
        date_of_joining = self.cleaned_data.get('date_of_joining')
        if date_of_joining and date_of_joining > timezone.now().date():
             raise forms.ValidationError("Date of joining cannot be in the future.")
        return date_of_joining

class AttendanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        self.fields['employee'].empty_label = "Select Employee"

    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'status']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        employee = cleaned_data.get('employee')
        
        if date and employee:
            if date < employee.date_of_joining:
                raise forms.ValidationError(f"Attendance date cannot be before employee's joining date ({employee.date_of_joining}).")
            if date > timezone.now().date():
                raise forms.ValidationError("Attendance date cannot be in the future.")
        return cleaned_data

class LoanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LoanForm, self).__init__(*args, **kwargs)
        self.fields['employee'].empty_label = "Select Employee"

    class Meta:
        model = Loan
        fields = ['employee', 'loan_amount', 'monthly_repayment', 'issue_date', 'status']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'loan_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'monthly_repayment': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount to deduct per month'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        issue_date = cleaned_data.get('issue_date')
        employee = cleaned_data.get('employee')
        
        if issue_date and employee:
            if issue_date < employee.date_of_joining:
                raise forms.ValidationError(f"Loan issue date cannot be before employee's joining date ({employee.date_of_joining}).")
            if issue_date > timezone.now().date():
                raise forms.ValidationError("Loan issue date cannot be in the future.")
        return cleaned_data

class PayrollAllowanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PayrollAllowanceForm, self).__init__(*args, **kwargs)
        self.fields['payroll'].empty_label = "Select Payroll Record"

    class Meta:
        model = Payroll_Allowance
        fields = ['payroll', 'name', 'amount']
        widgets = {
            'payroll': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PayrollDeductionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PayrollDeductionForm, self).__init__(*args, **kwargs)
        self.fields['payroll'].empty_label = "Select Payroll Record"

    class Meta:
        model = Payroll_Deduction
        fields = ['payroll', 'name', 'amount']
        widgets = {
            'payroll': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PayrollEditForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ['basic_salary', 'total_allowances', 'total_deductions', 'net_salary']
        widgets = {
            'basic_salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'total_allowances': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'total_deductions': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'net_salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
