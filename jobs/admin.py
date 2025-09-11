from django.contrib import admin
from .models import Jobs,JobApplication
# Register your models here.
class JobsAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'requirements','posted_by']

admin.site.register(Jobs,JobsAdmin)

class applicationAdmin(admin.ModelAdmin):
    list_display = ['jobs_title', 'seeker', 'letter']

    def jobs_title(self,obj):
        return obj.job.title
    
    def patient_name(self,obj):
        return obj.seeker.user.first_name
    
admin.site.register(JobApplication,applicationAdmin)