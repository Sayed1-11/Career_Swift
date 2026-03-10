from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('employee/', views.EmployerLandingView.as_view(), name='employee'),
    path('register/', views.EmployeeRegistrationView.as_view(), name='employee_register'),
    path('login/', views.EmployeeLoginView.as_view(), name='employee_login'),
    path('recruiter-registration/', views.BecomeEmployee.as_view(), name='recruiter_registration'),
    path('dashboard/', views.EmployeeDashboardView.as_view(), name='employee_dashboard'),
    path('settings/', views.EmployeeSettingsUpdateView.as_view(), name='employee_settings'),
    path('applications/', views.EmployeeApplicationsListView.as_view(), name='employee_applications'),
]
