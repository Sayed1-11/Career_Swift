from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('login/',views.Login.as_view(),name='login'),
    path('registration/',views.Registrationview.as_view(),name='registration'),
    path('profile/',views.profile.as_view(),name='profile'),
    path('Logout/',views.Logout.as_view(),name='Logout'),
    path('active/<uid64>/<token>/',views.activate,name='activate'),
]
