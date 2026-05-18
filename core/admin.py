from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Department, Designation, Employee, Attendance, Payroll, Payroll_Allowance, Payroll_Deduction, Loan, Loan_Payment, Payslip

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

    fieldsets = UserAdmin.fieldsets

    add_fieldsets = UserAdmin.add_fieldsets


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'department', 'designation', 'status')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('department', 'designation', 'status')

class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month', 'year', 'net_salary', 'generated_date')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Attendance)
admin.site.register(Payroll, PayrollAdmin)
admin.site.register(Payroll_Allowance)
admin.site.register(Payroll_Deduction)
admin.site.register(Loan)
admin.site.register(Loan_Payment)
admin.site.register(Payslip)
