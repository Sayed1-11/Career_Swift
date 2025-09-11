from django.contrib import admin
from .models import Contact_us
# Register your models here.
class Contact_us_Admin(admin.ModelAdmin):
    list_display = ["name","phone","message"]
admin.site.register(Contact_us,Contact_us_Admin)
