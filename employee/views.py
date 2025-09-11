from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import CreateView,ListView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Employee
from .forms import Employeeform

class BecomeEmployee(LoginRequiredMixin, CreateView):
    template_name = 'employee.html'
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
