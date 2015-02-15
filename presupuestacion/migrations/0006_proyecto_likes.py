# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('presupuestacion', '0005_auto_20150211_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='likes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
