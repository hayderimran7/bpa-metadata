from django.db import models
from django.contrib.auth.models import AbstractUser

class BPAUser(AbstractUser):
    """
    Custom BPA User with extra fields
    """
        
    department = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    affiliations = models.CharField(max_length=200, blank=True)
    note = models.TextField(blank=True)
