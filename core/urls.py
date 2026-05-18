from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Employee Portal
    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('my-profile/', views.employee_profile, name='employee_profile'),
    path('my-salary/', views.employee_salary, name='employee_salary'),

    
    # Employee Management
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('employees/edit/<int:pk>/', views.employee_edit, name='employee_edit'),
    path('employees/delete/<int:pk>/', views.employee_delete, name='employee_delete'),
    
    # Master Data
    path('departments/', views.department_list, name='department_list'),
    path('designations/', views.designation_list, name='designation_list'),
    
    # Attendance
    path('attendance/', views.attendance_list, name='attendance_list'),

    # Allowances & Deductions
    path('allowances/', views.allowance_list, name='allowance_list'),
    path('deductions/', views.deduction_list, name='deduction_list'),
    
    # Payroll
    path('payroll/', views.payroll_list, name='payroll_list'),
    path('payroll/generate/', views.payroll_generate, name='payroll_generate'),
    path('payroll/edit/<int:pk>/', views.payroll_edit, name='payroll_edit'),
    path('payslip/<int:payroll_id>/', views.payslip_view, name='payslip_view'),
    
    # Loans
    path('loans/', views.loan_list, name='loan_list'),
    path('loan-payments/', views.loan_payment_list, name='loan_payment_list'),
    path('salary-details/', views.salary_list, name='salary_list'),
]
