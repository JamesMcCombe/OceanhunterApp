from django.db import models
from django.contrib.auth.models import User
from annoying.fields import AutoOneToOneField

AREA_CHOICES = (('north', 'North',), ('south', 'South',))
GENDER_CHOICES = (('female', 'Female',), ('male', 'Male',))

class Profile(models.Model):
    user = AutoOneToOneField(User)
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    area = models.CharField(max_length=50, choices=AREA_CHOICES)
    city = models.CharField(max_length=50)
    dob = models.DateField()
    points = models.IntegerField(default=0)


TEAM_KINDS = (
    ('open', 'Open'),
    ('family', 'Family'),
)

class Team(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="team_logos", blank=True, null=True)
    kind = models.CharField(max_length=10, choices=TEAM_KINDS)

    # creater is default admin, but can transfer to some one else
    admin = models.ForeignKey(User, related_name='+') 
    users = models.ManyToManyField(User, related_name='+')
    points = models.IntegerField(default=0)
    text = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class Invite(models.Model):
    inviter = models.ForeignKey(User, related_name='invited_users')
    invitee = models.ForeignKey(User, related_name='+', null=True)

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
