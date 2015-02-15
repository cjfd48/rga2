# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('presupuestacion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='slug',
            field=models.SlugField(unique=True, default=''),
            preserve_default=False,
        ),
    ]
