from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import CreateView,ListView,View,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import JobSeekerForm
from .models import Job_seeker

class SeekerCreateView(CreateView,LoginRequiredMixin):
    model = Job_seeker
    form_class = JobSeekerForm
    template_name = 'job_seeker.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SeekerUpdateView(UpdateView):
    model = Job_seeker
    form_class = JobSeekerForm
    template_name = 'profile.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
