# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20151020_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fish',
            name='weight',
            field=models.DecimalField(max_digits=5, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='species',
            name='base',
            field=models.DecimalField(help_text=b'Base of calculating points', null=True, max_digits=5, decimal_places=3, blank=True),
        ),
    ]
