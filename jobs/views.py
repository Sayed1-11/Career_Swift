from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.views.generic import CreateView,ListView,View,FormView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from job_seeker.models import Job_seeker
from .forms import JobsForm,ApplicationForm
from .models import Jobs,JobApplication
from datetime import datetime
from django.contrib.auth.models import User
from employee.models import Employee
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from core.models import NewsletterSubscriber

def send_transaction_email(user, subject, template,seeker=None,letter=None):
        message = render_to_string(template, {
            'user' : user,
            'letter': letter,
            'seeker': seeker,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
  
        send_email.attach_alternative(message, "text/html")
        send_email.send()

def send_jobs_notification_email(user, subject, template,job=None):
        message = render_to_string(template, {
            'user' : user,
            'job':job,
            
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
  
        send_email.attach_alternative(message, "text/html")
        send_email.send()

class JobsView(LoginRequiredMixin, CreateView):
    template_name = 'jobs.html'
    form_class  = JobsForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = Employee.objects.get(user=self.request.user)
        return context

    def dispatch(self, request, *args, **kwargs):
        if not Employee.objects.filter(user=request.user).exists():
            messages.error(request, "Only employers can post jobs. Please register as an employer.")
            return redirect('employee_register')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        employee = get_object_or_404(Employee,user = self.request.user)
        form.instance.posted_by = employee
        subject = 'New Job Posted'
        template = 'job_post_notification.html' 
        job = form.instance
        users = User.objects.all()
        new = NewsletterSubscriber.objects.all()
        for news in new:
            for user in users:
                if user.email or news.email :
                    send_jobs_notification_email(
                        user=user or new,  
                        subject=subject,
                        template=template,
                        job=job
                    )
        return super().form_valid(form)
        
    
class AppliedView(LoginRequiredMixin, FormView):
    template_name = 'applied.html'
    form_class = ApplicationForm
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if Employee.objects.filter(user=request.user).exists():
            messages.error(request, "Employers cannot apply for jobs.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        job_id = self.kwargs['job_id']
        job = get_object_or_404(Jobs, pk=job_id)
        letter = form.cleaned_data['letter']
        Seeker, created = Job_seeker.objects.get_or_create(user=self.request.user)
        
        applied, created = JobApplication.objects.get_or_create(
                job=job,
                seeker=Seeker,
                letter=letter,
                CareerObjective = Seeker.CareerObjective,
                projects_name = Seeker.projects_name,
                Experience = Seeker.Experience,
                about_me = Seeker.about_me,
                Contact = Seeker.Contact,
                github_link = Seeker.github_link,
                others_link = Seeker.others_link,
                applied=datetime.now(),
            )
        applied.skills.set(Seeker.skills.all())
        messages.success(self.request,"Application Successfully applied")
        send_transaction_email(job.posted_by.user, "Applied for you job", "applied_mail.html",letter=letter,seeker=Seeker)
        

        return super().form_valid(form)
        
class joblist(LoginRequiredMixin,ListView):
        template_name = "joblist.html"
        model = JobApplication

        def get_queryset(self):
            
            queryset = super().get_queryset().filter(
                seeker__user=self.request.user
            )
            print(queryset)
            start_date_str = self.request.GET.get('start_date')
            end_date_str = self.request.GET.get('end_date')

            if start_date_str and end_date_str :
                start_date = datetime.strptime(start_date_str,"%Y-%m-%d").date()
                end_date = datetime.strptime(end_date_str,"%Y-%m-%d").date()
                queryset = queryset.filter(applied__date__gte = start_date,applied__date__lte = end_date )
            
            
            return queryset.distinct()
        
class jobdetails(LoginRequiredMixin,ListView):
        template_name = "job_details.html"
        model = Jobs

        def get_queryset(self):
            
            queryset = super().get_queryset().filter(
                posted_by__user=self.request.user
            )
            print(queryset)
            start_date_str = self.request.GET.get('start_date')
            end_date_str = self.request.GET.get('end_date')

            if start_date_str and end_date_str :
                start_date = datetime.strptime(start_date_str,"%Y-%m-%d").date()
                end_date = datetime.strptime(end_date_str,"%Y-%m-%d").date()
                queryset = queryset.filter(created_on__date__gte = start_date,created_on__date__lte = end_date )
            
            
            return queryset.distinct()
        
class jobsUpdate(LoginRequiredMixin,UpdateView):
    model = Jobs
    template_name = 'job_update.html'
    form_class = JobsForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = get_object_or_404(Employee, user=self.request.user)
        context['employee'] = employee
        return context

    def form_valid(self, form):
        employee = get_object_or_404(Employee,user = self.request.user)
        form.instance.posted_by = employee
        return super().form_valid(form)
    
    
