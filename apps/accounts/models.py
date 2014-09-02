from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User)
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)
    # add more fileds here...
