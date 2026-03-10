from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from .forms import RegistrationForm, ChangeUserForm, EmailAuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from job_seeker.models import Job_seeker
from job_seeker.forms import JobSeekerProfileForm, JobSeekerForm
from .models import UserProfile


# ── Registration ─────────────────────────────────────────────────────────────

class Registrationview(FormView):
    """Candidate self-registration with email confirmation."""
    template_name = 'register.html'
    form_class    = RegistrationForm
    success_url   = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # Profile is created inside RegistrationForm.save(), but since we
        # passed commit=False we need to create it manually here.
        UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': UserProfile.CANDIDATE},
        )

        # Send activation email
        token        = default_token_generator.make_token(user)
        uid          = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_link = f"http://127.0.0.1:8000/active/{uid}/{token}"
        email_subject = "Confirm Email"
        email_body    = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
        email = EmailMultiAlternatives(email_subject, "", to=[user.email])
        email.attach_alternative(email_body, "text/html")
        email.send()
        messages.info(self.request, "Please check your email to activate your account.")
        return redirect('login')


# ── Login ─────────────────────────────────────────────────────────────────────

class Login(LoginView):
    template_name = 'login.html'
    form_class    = EmailAuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """Route to the employer dashboard or home based on the user's role."""
        user = self.request.user
        try:
            if user.profile.is_employer:
                return reverse_lazy('jobdetails')
        except UserProfile.DoesNotExist:
            pass
        return reverse_lazy('home')


# ── Logout ────────────────────────────────────────────────────────────────────

class Logout(LoginRequiredMixin, LogoutView):
    def get_success_url(self):
        return reverse_lazy('home')


# ── Profile ───────────────────────────────────────────────────────────────────

class profile(LoginRequiredMixin, View):
    template_name = 'profile.html'

    def get(self, request):
        form        = ChangeUserForm(instance=request.user)
        job_seeker, _ = Job_seeker.objects.get_or_create(user=request.user)
        profile_form  = JobSeekerProfileForm(instance=job_seeker)
        resume_form   = JobSeekerForm(instance=job_seeker)
        return render(request, self.template_name, {
            'form':         form,
            'profile_form': profile_form,
            'resume_form':  resume_form,
            'job_seeker':   job_seeker,
        })

    def post(self, request):
        form        = ChangeUserForm(request.POST, instance=request.user)
        job_seeker, _ = Job_seeker.objects.get_or_create(user=request.user)
        profile_form  = JobSeekerProfileForm(instance=job_seeker)
        resume_form   = JobSeekerForm(instance=job_seeker)

        if 'profile_picture' in request.FILES:
            profile_form = JobSeekerProfileForm(request.POST, request.FILES, instance=job_seeker)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile picture updated successfully!")
                return redirect('profile')

        if 'Resume' in request.FILES:
            resume_form = JobSeekerForm(request.POST, request.FILES, instance=job_seeker)
            if resume_form.is_valid():
                resume_form.save()
                messages.success(request, "Resume uploaded successfully!")
                return redirect('profile')

        if 'first_name' in request.POST or 'last_name' in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, "Profile information updated!")
                return redirect('profile')

        return render(request, self.template_name, {
            'form':         form,
            'profile_form': profile_form,
            'resume_form':  resume_form,
            'job_seeker':   job_seeker,
        })


# ── Email activation ──────────────────────────────────────────────────────────

def activate(request, uid64, token):
    try:
        uid  = force_str(urlsafe_base64_decode(uid64))
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated. Please log in.")
        return redirect('login')

    messages.error(request, "Activation link is invalid or has expired.")
    return redirect('registration')
