# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-19 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0005_auto_20170518_1553"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, unique=True)),
            ],
            options={
                "verbose_name_plural": "Tags",
                "verbose_name": "Tag",
            },
        ),
        migrations.AddField(
            model_name="book",
            name="summary",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="book",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="books", to="books.Tag"
            ),
        ),
    ]
