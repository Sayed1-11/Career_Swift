from django.views.generic import CreateView, ListView, View, TemplateView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect
from account.forms import EmailAuthenticationForm
from .models import Employee
from jobs.models import Jobs, JobApplication
from .forms import Employeeform, EmployeeRegistrationForm

class EmployeeDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'employee_dashboard.html'
    context_object_name = 'jobs'

    def test_func(self):
        return Employee.objects.filter(user=self.request.user).exists()

    def handle_no_permission(self):
        messages.error(self.request, "You must be registered as an employer to access the dashboard.")
        return redirect('employee_register')

    def get_queryset(self):
        # Only show jobs posted by the logged-in employee
        try:
            employee = self.request.user.employees
            return Jobs.objects.filter(posted_by=employee).order_by('-created_on')
        except Employee.DoesNotExist:
            return Jobs.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            employee = self.request.user.employees
            jobs = self.get_queryset()
            
            context['employee'] = employee
            context['total_jobs'] = jobs.count()
            
            # Count total applications for all jobs posted by this employer
            total_apps = JobApplication.objects.filter(job__posted_by=employee).count()
            context['total_applications'] = total_apps
            
            # Calculate average applications
            if context['total_jobs'] > 0:
                context['avg_applications'] = round(total_apps / context['total_jobs'], 1)
            else:
                context['avg_applications'] = 0
            
            # Get latest 5 applications
            context['recent_applications'] = JobApplication.objects.filter(
                job__posted_by=employee
            ).order_by('-applied')[:5]
            
        except Employee.DoesNotExist:
            context['employee'] = None
            context['total_jobs'] = 0
            context['total_applications'] = 0
            context['recent_applications'] = []
            
        return context

class EmployerLandingView(TemplateView):
    template_name = 'employee.html'

class EmployeeRegistrationView(FormView):
    template_name = 'employee_register.html'
    form_class = EmployeeRegistrationForm
    success_url = reverse_lazy('employee_login')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, "Employer account created successfully! Please login.")
        return super().form_valid(form)

class EmployeeLoginView(LoginView):
    template_name = 'employee_login.html'
    form_class    = EmailAuthenticationForm
    
    def get_success_url(self):
        return reverse_lazy('employee_dashboard') # Redirect to employer dashboard

class BecomeEmployee(LoginRequiredMixin, CreateView):
    template_name = 'recruiter_registration.html'
    form_class  = Employeeform
    success_url = reverse_lazy('home')

    def form_valid(self, form) :
        employee_exist = Employee.objects.filter(user = self.request.user).exists()
        if employee_exist :
            messages.error(self.request,"You are already a employee")
            return redirect('home')
        else:
            form.instance.user = self.request.user
            return super().form_valid(form)

class EmployeeSettingsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Employee
    form_class = Employeeform
    template_name = 'employee_settings.html'
    success_url = reverse_lazy('employee_dashboard')

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_object(self, queryset=None):
        return self.request.user.employees

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = self.request.user.employees
        return context

    def form_valid(self, form):
        messages.success(self.request, "Company profile updated successfully!")
        return super().form_valid(form)

class EmployeeApplicationsListView(LoginRequiredMixin, ListView):
    model = JobApplication
    template_name = 'employee_applications.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return JobApplication.objects.filter(job__posted_by__user=self.request.user).order_by('-applied')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = self.request.user.employees
        return context
