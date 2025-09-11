from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='employees')
    company_name = models.CharField(max_length=70)
    Company_Logo = models.ImageField(upload_to='media/images',null=True)
    Company_number = models.CharField(max_length=11,null=True)
    About = models.TextField(blank=True)
    website = models.URLField(blank=True)
    company_mail = models.EmailField(null=True)

    def __str__(self) -> str:
        return self.company_name
