from django.db import models

# Create your models here.
class Contact_us(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=12)
    message = models.TextField()

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Contact Us"
