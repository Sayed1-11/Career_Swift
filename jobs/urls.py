
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('JobsView/',views.JobsView.as_view(),name='jobs'),
    path('joblist/',views.joblist.as_view(),name='joblist'),
    path('jobdetails/',views.jobdetails.as_view(),name='jobdetails'),
    path('apply/<int:job_id>',views.AppliedView.as_view(),name='apply'),
    path('jobupate/<int:pk>',views.jobsUpdate.as_view(),name='jobupate'),

    
]
