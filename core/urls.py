from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('industry/<slug:industry>',views.HomeView.as_view(),name='industry'),
    path('details/<int:id>',views.Details.as_view(),name='details'),
    path('subsribe/',views.Subsribe.as_view(),name='subsribe'),

    
]
