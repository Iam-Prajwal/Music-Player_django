from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Define fields
    name = models.CharField(max_length=20, default='UserName')
    email = models.EmailField(max_length=254, unique=True)
    
    # Make 'username' optional or remove it, but keep the field definition.
    username = models.CharField(max_length=150, blank=True, null=True)
    
    # Keep other custom fields
    usr_phone = models.CharField(max_length=20)
    usr_gender = models.CharField(max_length=10)
    profile_pic = models.FileField(upload_to='profile/', default='profile/team.jpg')

    # Set 'email' as the unique identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Include username in REQUIRED_FIELDS for superuser creation
