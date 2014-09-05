from django.db import models
from django.contrib.auth.models import User
from annoying.fields import AutoOneToOneField

class Profile(models.Model):
    user = AutoOneToOneField(User)
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)
    # add more fileds here...

class Team(models.Model):
    name = models.CharField(max_length=50)
    KINDS = (
        ('open', 'Open'),
        ('family', 'Family'),
    )
    kind = models.CharField(max_length=10, choices=KINDS)

    # creater is default admin, but can transfer to some one else
    admin = models.ForeignKey(User) 
    users = models.ManyToManyField(User)
    points = models.IntegerField(default=0)
    text = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class Invite(models.Model):
    inviter = models.ForeignKey(User)
    invitee = models.ForeignKey(User, null=True)

    create = models.DateTimeField(auto_now_add=True)
    read = models.DateTimeField(editable=False, null=True, help_text='when was this invite been read')
    accept = models.DateTimeField(editable=False, null=True, help_text='when was this invite been accepted')

    STATUS = (
        ('new', 'New'),
        ('read', 'Read'),
        ('accepted', 'Accepted'),
        ('removed', 'Removed'),
    )
    status = models.CharField(max_length=10, choices=STATUS, default='new')

    INVITE_VIA = (
        ('email', 'Email'),
        ('fb', 'Facebook'),
    )
    via = models.CharField(max_length=10, default='email')
    ref = models.CharField(max_length=30) # email or social id
    text = models.TextField(blank=True)

    def __unicode__(self):
        return 'Invitation from %s' % self.inviter.first_name
