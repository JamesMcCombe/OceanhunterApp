import hashlib
import datetime
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.template import Context, loader
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver

from annoying.fields import AutoOneToOneField
from apps.main.models import Division, Fish


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
        ('Chathams Islands', 'Chathams Islands'),
    )),
)


class Profile(models.Model):
    user = AutoOneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    division = models.ForeignKey(Division, blank=False, null=True, on_delete=models.SET_NULL)
    dob = models.DateField(null=True)

    def biggest_fish(self):
        return self.user.fish_set.order_by('-points').first()

    def facebook_binded(self):
        return self.user.social_auth.filter(provider="facebook").count() > 0

    def is_new(self):
        have_fish = self.user.fish_set.count() > 0

        _now = timezone.now()
        new_join = (_now - self.user.date_joined).seconds < 600 # 10 mins

        return not have_fish and new_join

    @property
    def profile_completed(self):
        return self.division is not None

    @property
    def points(self):
        return self.user.fish_set.exclude(species__name='Kingfish').aggregate(total_points=Sum('points'))['total_points']

    def get_species(self):
        from apps.main.models import Species
        qs = self.division.species.all() | Species.objects.filter(name__in=['Kingfish'])
        qs = qs.distinct()
        return qs


@receiver(post_save, sender=Profile)
def send_welcome_email(sender, instance, created, **kwargs):
    u = instance.user
    if created and u.email:
        email = f'{u.first_name} {u.last_name} <{u.email}>'
        t = loader.get_template('emails/welcome-inline.html')
        subject = 'Ocean Hunter Spearfishing Competition 2016/17'
        c = Context({'SITE_URL': settings.SITE_URL, 'subject': subject, 'user': u})
        html_content = t.render(c)
        msg = EmailMessage(subject, html_content, settings.DEFAULT_FROM_EMAIL, [email])
        msg.content_subtype = "html"
        msg.send()


TEAM_KINDS = (
    ('family', 'Family Team'),
    ('open', 'Open Team'),
)

class Team(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="team_logos", blank=True, null=True)
    admin = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    users = models.ManyToManyField(User)
    text = models.TextField(blank=True)

    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def recalculate_points(self):
        pass

    def biggest_fish(self):
        return Fish.objects.filter(user__in=self.users.all()).order_by('-points').first()

    @property
    def points(self):
        return sum([u.profile.points for u in self.users.all() if u.profile.points])


class Invite(models.Model):
    inviter = models.ForeignKey(User, related_name='invited_users', on_delete=models.CASCADE)
    invitee = models.ForeignKey(User, related_name='+', null=True, on_delete=models.SET_NULL)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

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
    ref = models.CharField(max_length=30)  # email or social id
    text = models.TextField(blank=True)
    key = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'Invitation from {self.inviter.first_name}'

    def save(self, **kwargs):
        if not self.pk:
            string = f'{self.inviter.pk}{self.ref}'
            self.key = hashlib.md5(string.encode('utf-8')).hexdigest()
        super().save(**kwargs)


class FacebookAdminToken(models.Model):
    access_token = models.TextField()
    obtained = models.DateTimeField(auto_now_add=True)
