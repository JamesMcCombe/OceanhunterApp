import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from annoying.fields import AutoOneToOneField
from main import models as mm

AREA_CHOICES = (('North Island', 'North Island',), ('South Island', 'South Island',))
GENDER_CHOICES = (('female', 'Female',), ('male', 'Male',))
CITY_CHOICES = (
    ('', 'Region'), # as a placeholder
    ('North Island', (
        ('Northland', 'Northland'),
        ('Auckland', 'Auckland'),
        ('Waikato', 'Waikato'),
        ('Bay of Plenty', 'Bay of Plenty'),
        ('Gisborne', 'Gisborne'),
        ("Hawke's Bay", "Hawke's Bay"),
        ('Taranaki', 'Taranaki'),
        ('Wanganui', 'Wanganui'),
        ('Manawatu', 'Manawatu'),
        ('Wairarapa', 'Wairarapa'),
        ('Wellington', 'Wellington'),
    )),
    ('South Island', (
        ('Nelson Bays', 'Nelson Bays'),
        ('Marlborough', 'Marlborough'),
        ('West Coast', 'West Coast'),
        ('Canterbury', 'Canterbury'),
        ('Timaru/Oamaru', 'Timaru/Oamaru'),
        ('Otago', 'Otago'),
        ('Southland', 'Southland'),
    )),
)

class Profile(models.Model):
    user = AutoOneToOneField(User)
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    area = models.CharField(max_length=50, choices=AREA_CHOICES)
    city = models.CharField(max_length=50, choices=CITY_CHOICES)
    dob = models.DateField(null=True)
    points = models.IntegerField(default=0)

    def save(self, *a, **kw):
        # get area of city
        for area, cities in CITY_CHOICES:
            for city in cities:
                if self.city == city[0]:
                    self.area = area
                    break

        super(Profile, self).save(*a, **kw)

    def recalculate_points(self):
        self.points = sum(f.points for f in self.user.fish_set.all())
        self.save()

    def biggest_fish(self):
        return self.user.fish_set.order_by('-points').first()

    def facebook_binded(self):
        return self.user.social_auth.filter(provider="facebook").count() > 0

    def is_new(self):
        have_fish = self.user.fish_set.count() > 0

        _now = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
        new_join = (_now - self.user.date_joined).seconds < 600 # 10 mins

        return not have_fish and new_join

TEAM_KINDS = (
    ('family', 'Family Team'),
    ('open', 'Open Team'),
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

    create = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def recalculate_points(self):
        self.points = sum(u.profile.points for u in self.users.all())
        self.save()

    def biggest_fish(self):
        return mm.Fish.objects \
            .filter(user=self.users.all()) \
            .order_by('-points') \
            .first()


class Invite(models.Model):
    inviter = models.ForeignKey(User, related_name='invited_users')
    invitee = models.ForeignKey(User, related_name='+', null=True)
    team = models.ForeignKey(Team)

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
