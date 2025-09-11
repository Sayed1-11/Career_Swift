from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ChangeUserForm(UserChangeForm):
    password=None
    class Meta:
        model = User
        fields = ['username','email']

