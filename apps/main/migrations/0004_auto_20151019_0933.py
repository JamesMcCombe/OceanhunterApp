# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_division'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='species',
            name='k',
        ),
        migrations.AlterField(
            model_name='species',
            name='base',
            field=models.IntegerField(help_text=b'Base of calculating points', null=True),
        ),
    ]
