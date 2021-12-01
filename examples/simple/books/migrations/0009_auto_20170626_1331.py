# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 18:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0008_book_state"),
    ]

    operations = [
        migrations.AddField(
            model_name="publisher",
            name="info",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="book",
            name="state",
            field=models.CharField(
                choices=[
                    ("published", "Published"),
                    ("not_published", "Not published"),
                    ("in_progress", "In progress"),
                    ("cancelled", "Cancelled"),
                    ("rejected", "Rejected"),
                ],
                default="published",
                max_length=100,
            ),
        ),
    ]
