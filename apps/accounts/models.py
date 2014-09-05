from django.db import models
from django.contrib.auth.models import User
from annoying.fields import AutoOneToOneField

ISLAND_CHOICES = (('north', 'North',), ('south', 'South',))
SEX_CHOICES = (('female', 'Female',), ('male', 'Male',))


class Profile(models.Model):
    user = AutoOneToOneField(User)
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)
    # add more fileds here...
    gender = models.CharField(max_length=255, choices=SEX_CHOICES)
    island = models.CharField(max_length=255, choices=ISLAND_CHOICES)
    city = models.CharField(max_length=255, )
    dob = models.DateField()
