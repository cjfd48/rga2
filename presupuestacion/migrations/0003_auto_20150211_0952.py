# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('presupuestacion', '0002_proyecto_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poste',
            name='nombre',
            field=models.CharField(max_length=128),
            preserve_default=True,
        ),
    ]
