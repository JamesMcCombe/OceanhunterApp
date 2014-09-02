from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    dob = models.DateField(blank=True,null=True)
    #TODO: add your fields here...
