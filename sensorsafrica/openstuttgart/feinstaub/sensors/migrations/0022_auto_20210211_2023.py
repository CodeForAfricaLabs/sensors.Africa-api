# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-02-11 20:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0021_auto_20210204_1106'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='sensorlocation',
            index=models.Index(fields=['country'], name='country_idx'),
        ),
        migrations.AddIndex(
            model_name='sensorlocation',
            index=models.Index(fields=['city'], name='city_idx'),
        ),
    ]
