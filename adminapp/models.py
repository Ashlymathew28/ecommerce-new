from django.db import models

# Create your models here.

class Banner(models.Model):
    images=models.ImageField(upload_to='media',blank=True)