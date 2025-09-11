from .models import Employee
from django import forms


class Employeeform(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['user']

    def __init__(self,*args, **kwargs):
        super(Employeeform, self).__init__(*args, **kwargs)
