# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-01 00:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0012_auto_20170630_1900"),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="company_website",
            field=models.URLField(blank=True, null=True),
        ),
    ]
