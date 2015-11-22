# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20151117_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='species',
            name='base',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=5, blank=True, help_text=b'Base of calculating points', null=True),
        ),
    ]
