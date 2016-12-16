# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20151102_0554'),
    ]

    operations = [
        migrations.AddField(
            model_name='invite',
            name='key',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
