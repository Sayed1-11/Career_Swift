from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
      path('contact/',views.Contact_us.as_view(),name='contact'),
      path('about/',views.About_us.as_view(),name='about'),
]