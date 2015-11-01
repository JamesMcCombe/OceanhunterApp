# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_profile_points'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='kind',
        ),
    ]
