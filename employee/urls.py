from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('employee/',views.BecomeEmployee.as_view(),name='employee'),

    
]
