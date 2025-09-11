from django.db import models
from django.contrib.auth.models import User
from location.models import Location

# Create your models here.

class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Job_seeker(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='seeker')
    Resume = models.FileField(upload_to='media/',null=True)


    def __str__(self) -> str:
        return self.user.username
