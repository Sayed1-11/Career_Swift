from django.shortcuts import render,redirect
from django.views.generic import FormView,TemplateView
from . forms import RegistrationForm,ChangeUserForm
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView,LogoutView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from job_seeker.models import Job_seeker
from django.contrib import messages
# Create your views here. 

class Registrationview(FormView):
    template_name = "register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        print("uid ",uid)
        confirm_link = f"http://127.0.0.1:8000/active/{uid}/{token}"
        email_subject = "Confirm Email"
        email_body = render_to_string('confirm_email.html',{'confirm_link': confirm_link})
        email = EmailMultiAlternatives(email_subject, "",to=[user.email])
        email.attach_alternative(email_body,"text/html")
        email.send()
        messages.error(self.request,"Please check your email to active your account")
        user.save()
        return super().form_valid(form)
    
class Login(LoginView):
    template_name="login.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self) -> str:
        return reverse_lazy('home')
    

class Logout(LoginRequiredMixin,LogoutView):
    def get_success_url(self) -> str:
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')
    

    

class profile(LoginRequiredMixin,View):
    template_name = 'profile.html'

    def get(self, request):
        form = ChangeUserForm(instance=request.user)
        jobs, _ = Job_seeker.objects.get_or_create(user=request.user)
        return render(request, self.template_name, {'form': form, 'jobs':jobs})

    def post(self, request):
        form = ChangeUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})
    

def activate(request,uid64,token):
    try :
        uid = force_str(urlsafe_base64_decode(uid64))
        print(uid)
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,"Account has been activated")
        return redirect('login')

    else:
        return redirect('registration')
