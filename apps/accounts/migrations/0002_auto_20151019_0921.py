# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_division'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='area',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='city',
        ),
        migrations.AddField(
            model_name='profile',
            name='division',
            field=models.ForeignKey(default=0, to='main.Division'),
            preserve_default=False,
        ),
    ]
