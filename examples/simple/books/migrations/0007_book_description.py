# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-19 10:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0006_auto_20170619_0428"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
