from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
# from app.views import user_directory_path





class User(AbstractUser):
    username=None
    email = models.EmailField(unique=True)
    phone_No =models.CharField(max_length=10)
    GENDER_CHOICES = (
        ('M', 'MALE'),
        ('F', 'FEMALE'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    address = models.TextField()
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]


class blogs(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    create= models.DateTimeField(auto_now_add=True)
    update= models.DateTimeField(null= True, blank=True)
    delete = models.DateTimeField(null= True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    trash = models.BooleanField(default=False)
    





    


    
    