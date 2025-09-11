from .models import Job_seeker
from django import forms
from django.core.exceptions import ValidationError


class JobSeekerForm(forms.ModelForm):
    class Meta:
        model = Job_seeker
        fields = ['Resume']
        widgets = {
            'Resume': forms.FileInput(attrs={
                'accept': '.pdf',
                'class': 'form-control'
            })
        }
    
    def clean_Resume(self):
        resume = self.cleaned_data.get('Resume')
        if resume:
            if not resume.name.lower().endswith('.pdf'):
                raise ValidationError("Only PDF files are allowed.")
            
            if resume.size > 5 * 1024 * 1024:
                raise ValidationError("File size must be less than 5MB.")
        
        return resume
