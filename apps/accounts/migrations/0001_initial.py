# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import annoying.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('read', models.DateTimeField(help_text=b'when was this invite been read', null=True, editable=False)),
                ('accept', models.DateTimeField(help_text=b'when was this invite been accepted', null=True, editable=False)),
                ('status', models.CharField(default=b'new', max_length=10, choices=[(b'new', b'New'), (b'read', b'Read'), (b'accepted', b'Accepted'), (b'removed', b'Removed')])),
                ('via', models.CharField(default=b'email', max_length=10)),
                ('ref', models.CharField(max_length=30)),
                ('text', models.TextField(blank=True)),
                ('invitee', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True)),
                ('inviter', models.ForeignKey(related_name='invited_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar', models.ImageField(null=True, upload_to=b'avatars', blank=True)),
                ('gender', models.CharField(max_length=10, choices=[(b'female', b'Female'), (b'male', b'Male')])),
                ('area', models.CharField(max_length=50, choices=[(b'North Island', b'North Island'), (b'South Island', b'South Island')])),
                ('city', models.CharField(max_length=50, choices=[(b'', b'Region'), (b'North Island', ((b'Northland', b'Northland'), (b'Auckland', b'Auckland'), (b'Waikato', b'Waikato'), (b'Bay of Plenty', b'Bay of Plenty'), (b'Gisborne', b'Gisborne'), (b"Hawke's Bay", b"Hawke's Bay"), (b'Taranaki', b'Taranaki'), (b'Wanganui', b'Wanganui'), (b'Manawatu', b'Manawatu'), (b'Wairarapa', b'Wairarapa'), (b'Wellington', b'Wellington'))), (b'South Island', ((b'Nelson Bays', b'Nelson Bays'), (b'Marlborough', b'Marlborough'), (b'West Coast', b'West Coast'), (b'Canterbury', b'Canterbury'), (b'Timaru/Oamaru', b'Timaru/Oamaru'), (b'Otago', b'Otago'), (b'Southland', b'Southland'), (b'Chathams Islands', b'Chathams Islands')))])),
                ('dob', models.DateField(null=True)),
                ('points', models.IntegerField(default=0)),
                ('user', annoying.fields.AutoOneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('logo', models.ImageField(null=True, upload_to=b'team_logos', blank=True)),
                ('kind', models.CharField(max_length=10, choices=[(b'family', b'Family Team'), (b'open', b'Open Team')])),
                ('points', models.IntegerField(default=0)),
                ('text', models.TextField(blank=True)),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('admin', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='invite',
            name='team',
            field=models.ForeignKey(to='accounts.Team'),
            preserve_default=True,
        ),
    ]
