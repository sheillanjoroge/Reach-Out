# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2021-02-01 14:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reach', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='reach',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reach.Hood'),
        ),
    ]
