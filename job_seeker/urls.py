
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('seeker/create/', views.SeekerCreateView.as_view(), name='seeker'),
    path('seeker/resume/delete/', views.delete_resume, name='delete_resume')
]
