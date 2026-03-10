from django.shortcuts import render,get_object_or_404,redirect,HttpResponseRedirect
from django.views.generic import DetailView,CreateView,ListView,View,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from jobs.models import Jobs
from job_seeker.models import Job_seeker
from category.models import Category
from contact_us.forms import Contactform
from jobs.forms import JobSearchForm
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import NewsletterSubscriber
# Create your views here.


def send_transaction_email(email, subject, template):
        message = render_to_string(template, { })
        send_email = EmailMultiAlternatives(subject, '', to=[email])
  
        send_email.attach_alternative(message, "text/html")
        send_email.send()


class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get(self, request, industry=None):
        industries = Category.objects.all()
        # Only get the latest 4 jobs for the homepage
        data = Jobs.objects.all().order_by('-created_on')

        applied_job_ids = []
        if request.user.is_authenticated:
            job, _ = Job_seeker.objects.get_or_create(user=request.user)
            from jobs.models import JobApplication
            applied_job_ids = JobApplication.objects.filter(seeker=job).values_list('job_id', flat=True)
        else:
            job = None

        context = {
            'data': data,
            'industry': industries,
            'jobs': job,
            'applied_job_ids': applied_job_ids,
        }
        return self.render_to_response(context)

class JobSearchView(TemplateView):
    template_name = 'job_search.html'
    paginate_by = 6
    
    def get(self, request, industry=None):
        industries = Category.objects.all()
        data = Jobs.objects.all().order_by('-created_on')
        job_title = request.GET.get('job-title', '')
        job_location = request.GET.get('job-location', '')
        category_slug = request.GET.get('category', '')

        if job_title:
            data = data.filter(title__icontains=job_title)
        if job_location:
            data = data.filter(location__name__icontains=job_location)

        if category_slug:
            try:
                industry_instance = Category.objects.get(slug=category_slug)
                data = data.filter(industry=industry_instance)
            except Category.DoesNotExist:
                pass
        elif industry is not None:
            try:
                industry_instance = Category.objects.get(slug=industry)
                data = data.filter(industry=industry_instance)
            except Category.DoesNotExist:
                pass

        applied_job_ids = []
        if request.user.is_authenticated:
            job, _ = Job_seeker.objects.get_or_create(user=request.user)
            from jobs.models import JobApplication
            applied_job_ids = JobApplication.objects.filter(seeker=job).values_list('job_id', flat=True)
        else:
            job = None

        paginator = Paginator(data, self.paginate_by)
        page = request.GET.get('page')
        try:
            jobs = paginator.page(page)
        except PageNotAnInteger:
            jobs = paginator.page(1)
        except EmptyPage:
            jobs = paginator.page(paginator.num_pages)

        context = {
            'data': jobs,
            'industry': industries,
            'jobs': job,
            'applied_job_ids': applied_job_ids,
            'search_query': {
                'job_title': job_title,
                'job_location': job_location,
            }
        }
        return self.render_to_response(context)

class Details(DetailView):
    model = Jobs
    pk_url_kwarg = 'id'
    template_name = "details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.object
        context['jobs'] = job
        
        has_applied = False
        if self.request.user.is_authenticated:
            try:
                seeker = self.request.user.job_seekers
                from jobs.models import JobApplication
                has_applied = JobApplication.objects.filter(job=job, seeker=seeker).exists()
            except:
                pass
        context['has_applied'] = has_applied
        return context
    
class Subsribe(FormView):
    def post(self, request,*args, **kwargs):
        email = request.POST.get('newsletter-name')
        news = NewsletterSubscriber.objects.create(email=email)
        news.save()
        send_transaction_email(email, "New Subsribtion", "subsribe_mail.html")

        return HttpResponseRedirect(reverse_lazy('home')) 
    
