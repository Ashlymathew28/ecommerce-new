from django.db import models
from .manager import UserManager
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.


class Account(AbstractBaseUser):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True,null=True)
    email=models.EmailField(max_length=100,unique=True)
    phone_number=models.CharField(max_length=50)
    blocked=models.BooleanField(default=False)


    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    is_superuser=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
  
    objects  = UserManager()
    USERNAME_FIELD='email'
    #REQUIRED_FIELDS= ['email']
        
    def __str__(self):
        return self.email
    def has_perm(self,perm,obj=None):
        return self.is_superuser
    def has_module_perms(self,add_label):
        return True