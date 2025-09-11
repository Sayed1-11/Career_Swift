from django.shortcuts import render
from .forms import Contactform
from django.views.generic import FormView,TemplateView
from django.urls import reverse_lazy
# Create your views here.
class Contact_us(FormView):
    template_name = "contact.html"
    form_class = Contactform
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

class About_us(TemplateView):
    template_name = "about.html"
