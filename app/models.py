from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
# from app.views import user_directory_path

class User(AbstractUser):
    username=None
    email = models.EmailField(unique=True)
    phone_No =models.CharField(max_length=10)
    gender = models.CharField(max_length=1)
    date_of_birth = models.DateField()
    address = models.TextField()
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]


class blogs(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    create= models.DateTimeField(auto_now_add=True)
    update= models.DateTimeField(null= True, blank=True)
    delete = models.DateTimeField(null= True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    upload = models.ImageField(null=True, blank=True)
    trash = models.BooleanField(default=False)
    





    


    
    