# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20151019_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='division',
            field=models.ForeignKey(to='main.Division', null=True),
        ),
    ]
