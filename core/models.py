from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Designation(models.Model):
    designation_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title

class User(AbstractUser):
    # AbstractUser already has username, password, last_login, first_name, last_name, email
    # We will override id to match user_id requirement
    user_id = models.AutoField(primary_key=True)
    
    
    # ROLE_CHOICES removed as role is deprecated


    def __str__(self):
        return self.username

class Employee(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    date_of_joining = models.DateField()
    
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Leave', 'Leave'),
    )
    
    attendance_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.employee} - {self.date} - {self.status}"

class Payroll(models.Model):
    payroll_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=20) # e.g., "January"
    year = models.IntegerField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    generated_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Payroll - {self.employee} - {self.month} {self.year}"

class Payroll_Allowance(models.Model):
    # id is auto created by Django as 'id' usually, but request says 'id (PK)'. 
    # Django default PK is 'id'.
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name='allowances')
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}: {self.amount}"

class Payroll_Deduction(models.Model):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name='deductions')
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name}: {self.amount}"

class Loan(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Closed', 'Closed'),
    )
    
    loan_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_repayment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    issue_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"Loan {self.loan_id} - {self.employee}"

class Loan_Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payments')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    payment_date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment {self.payment_id} - {self.amount}"

class Payslip(models.Model):
    payslip_id = models.AutoField(primary_key=True)
    payroll = models.OneToOneField(Payroll, on_delete=models.CASCADE)
    generated_date = models.DateField(default=timezone.now)
    pdf_path = models.CharField(max_length=255) # Storing path relative to MEDIA_ROOT

    def __str__(self):
        return f"Payslip for {self.payroll}"
