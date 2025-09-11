from django.db import models

# Create your models here.
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
