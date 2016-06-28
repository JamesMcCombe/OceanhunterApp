# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20151123_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fish',
            name='points',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=3),
        ),
    ]
