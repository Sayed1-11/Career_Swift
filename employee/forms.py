from .models import Employee
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from account.models import UserProfile


class Employeeform(forms.ModelForm):
    """Form for an already-authenticated user to fill in company details."""
    class Meta:
        model   = Employee
        exclude = ['user']


class EmployeeRegistrationForm(UserCreationForm):
    """
    Employer self-registration form.
    Creates a User + Employee profile + UserProfile(role=EMPLOYER).
    Username is derived from the email address.
    """
    first_name     = forms.CharField(max_length=30, required=True)
    last_name      = forms.CharField(max_length=30, required=True)
    email          = forms.EmailField(required=True)
    company_name   = forms.CharField(max_length=70, required=True)
    company_mail   = forms.EmailField(required=True)
    company_number = forms.CharField(max_length=11, required=False)
    website        = forms.URLField(required=False)
    about          = forms.CharField(widget=forms.Textarea, required=False)
    company_logo   = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
            # Create the company profile
            Employee.objects.create(
                user           = user,
                company_name   = self.cleaned_data.get('company_name'),
                company_mail   = self.cleaned_data.get('company_mail'),
                Company_number = self.cleaned_data.get('company_number'),
                website        = self.cleaned_data.get('website'),
                About          = self.cleaned_data.get('about'),
                Company_Logo   = self.cleaned_data.get('company_logo'),
            )
            # Assign EMPLOYER role
            UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': UserProfile.EMPLOYER},
            )
        return user
