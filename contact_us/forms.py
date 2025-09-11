from .models import Contact_us
from django import forms


class Contactform(forms.ModelForm):
    class Meta:
        model = Contact_us
        fields = '__all__'

    def __init__(self,*args, **kwargs):
        super(Contactform, self).__init__(*args, **kwargs)