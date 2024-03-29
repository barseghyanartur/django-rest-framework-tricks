# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-14 15:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0015_auto_20170713_0418"),
    ]

    operations = [
        migrations.AlterField(
            model_name="publisher",
            name="address",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="publisher",
            name="city",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="publisher",
            name="country",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="publisher",
            name="state_province",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
