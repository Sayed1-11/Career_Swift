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
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    CareerObjective = models.TextField(null=True, blank=True)
    projects_name = models.TextField(null=True, blank=True)
    Experience = models.TextField(null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    Contact = models.CharField(max_length=12,null=True, blank=True)
    github_link = models.CharField(max_length=500,null=True, blank=True)
    others_link = models.CharField(max_length=256,null=True,blank=True)
    skills = models.ManyToManyField(Skill, blank=True)


    def __str__(self) -> str:
        return self.user.username
