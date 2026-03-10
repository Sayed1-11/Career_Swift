from .models import Jobs,JobApplication
from employee.models import Employee
from django import forms


class JobsForm(forms.ModelForm):
    class Meta:
        model = Jobs
        exclude= ['posted_by']
    def __init__(self,*args, **kwargs):
        super(JobsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control rounded-3',
                'placeholder': f'Enter {field.replace("_", " ")}'
            })


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['letter']
        
    def __init__(self,*args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)

class JobSearchForm(forms.Form):
    job_title = forms.CharField(label='Job Title', max_length=100, required=True)
    job_location = forms.CharField(label='Location', max_length=100, required=True)

   
