import datetime
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.template import Context, RequestContext, loader
from django.core.mail import EmailMessage, send_mail, mail_managers
from django.db.models.signals import post_save
from django.dispatch import receiver

from annoying.fields import AutoOneToOneField
from apps.main.models import Division


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
    user = AutoOneToOneField(User)
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    # area = models.CharField(max_length=50, choices=AREA_CHOICES)
    # city = models.CharField(max_length=50, choices=CITY_CHOICES)
    division = models.ForeignKey(Division, blank=False, null=True)
    dob = models.DateField(null=True)
    # points = models.IntegerField(default=0)

    def recalculate_points(self):
        species_in_count = {
            'North Island': (
                'Snapper',
                'Butter Fish',
                'Tarakihi',
                'Kahawai',
                'Giant Boarfish',
                'Pink Maomao',
            ),
            'South Island': (
                'Blue Cod',
                'Butter Fish',
                'Trumpeter',
                'Blue Moki',
                'Kahawai',
                'Tarakihi',
            ),
        }
        self.points = sum(
            f.points
            for f in self.user.fish_set.all()
            if f.species.name in species_in_count[self.area]
        )
        self.save()
        for team in self.user.team_set.all():
            team.recalculate_points()

    def biggest_fish(self):
        return self.user.fish_set.order_by('-points').first()

    def facebook_binded(self):
        return self.user.social_auth.filter(provider="facebook").count() > 0

    def is_new(self):
        have_fish = self.user.fish_set.count() > 0

        _now = timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
        new_join = (_now - self.user.date_joined).seconds < 600 # 10 mins

        return not have_fish and new_join

    @property
    def profile_completed(self):
        return self.division

    @property
    def points(self):
        return self.user.fish_set.aggregate(total_points=Sum('points'))['total_points']

    def get_species(self):
        from apps.main.models import Species
        qs = self.division.species.all() | Species.objects.filter(name__in=['Kingfish', 'Crayfish'])
        return qs

# send welcome email
@receiver(post_save, sender=Profile)
def send_welcome_email(sender, instance, created, **kwargs):
    u = instance.user
    if created and u.email:
        email = '%s %s <%s>' % (u.first_name, u.last_name, u.email)
        t = loader.get_template('emails/welcome-inline.html')
        subject = 'Ocean Hunter Spearfishing Competition 2014/15'
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
    kind = models.CharField(max_length=10, choices=TEAM_KINDS)

    # creater is default admin, but can transfer to some one else
    admin = models.ForeignKey(User, related_name='+')
    users = models.ManyToManyField(User)
    points = models.IntegerField(default=0)
    text = models.TextField(blank=True)

    create = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def recalculate_points(self):
        self.points = sum(u.profile.points for u in self.users.all()) / self.users.count()
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



