# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20151019_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='division',
            name='species',
            field=models.ManyToManyField(related_name='division', to='main.Species'),
        ),
        migrations.AlterField(
            model_name='fish',
            name='points',
            field=models.DecimalField(default=0, max_digits=6, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='fish',
            name='weight',
            field=models.DecimalField(max_digits=6, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='species',
            name='base',
            field=models.DecimalField(help_text=b'Base of calculating points', null=True, max_digits=6, decimal_places=3, blank=True),
        ),
        migrations.AlterField(
            model_name='species',
            name='logo',
            field=models.ImageField(null=True, upload_to=b'species'),
        ),
    ]
