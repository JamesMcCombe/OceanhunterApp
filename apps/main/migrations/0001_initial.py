# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=2000)),
                ('create', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.DecimalField(max_digits=5, decimal_places=2)),
                ('witness', models.CharField(max_length=50)),
                ('points', models.IntegerField(default=0)),
                ('image', models.ImageField(upload_to=b'fish')),
                ('status', models.CharField(default=b'normal', max_length=10, choices=[(b'normal', b'Normal'), (b'removed', b'Removed')])),
                ('create', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Fish',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('logo', models.ImageField(upload_to=b'species')),
                ('k', models.IntegerField(help_text=b'Weight of calculating points')),
                ('base', models.IntegerField(help_text=b'Base of calculating points')),
            ],
            options={
                'verbose_name_plural': 'Species',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='fish',
            name='species',
            field=models.ForeignKey(to='main.Species'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fish',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='fish',
            field=models.ForeignKey(to='main.Fish'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
