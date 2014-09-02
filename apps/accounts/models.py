from django.db import models
from django.contrib.auth.models import User
from annoying.fields import AutoOneToOneField

class Profile(models.Model):
    user = AutoOneToOneField(User)
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)
    # add more fileds here...
