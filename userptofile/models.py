from django.db import models
from accounts.models import Account
# Create your models here.


class Address(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    fname = models.CharField(max_length=50,null=False)
    lname = models.CharField(max_length=100,null=False)
    email = models.CharField(max_length=300,null=False)
    Address = models.CharField(max_length=300,null=False)
    city = models.CharField(max_length=100,null = False)
    state = models.CharField(max_length=100,null=False)
    country = models.CharField(max_length=100,null=False)
    pincode = models.IntegerField(null=False)