from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import UserProfile


class EmailAuthenticationForm(AuthenticationForm):
    """
    Overrides the default Django AuthenticationForm to accept an
    email address in the username field instead of enforcing username
    validation formats.
    """
    username = forms.CharField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'})
    )

    error_messages = {
        'invalid_login': (
            "Please enter a correct email address and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': ("This account is inactive."),
    }



class RegistrationForm(UserCreationForm):
    """
    Candidate self-registration form.
    Creates a User + UserProfile(role=CANDIDATE).
    Username is derived from the email address.
    """
    first_name = forms.CharField(max_length=30, required=True)
    last_name  = forms.CharField(max_length=30, required=True)
    email      = forms.EmailField(required=True)

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the auto-generated username field – we use email instead.
        self.fields.pop('username', None)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # email → username
        if commit:
            user.save()
            UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': UserProfile.CANDIDATE},
            )
        return user


class ChangeUserForm(UserChangeForm):
    """Read-only display form for the user's own profile page."""
    password   = None
    first_name = forms.CharField(max_length=30)
    last_name  = forms.CharField(max_length=30)
    email      = forms.EmailField()

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True
            field.widget.attrs['class']    = 'form-control bg-light'
