# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2020-09-19 11:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='postal_coad',
            new_name='postal_code',
        ),
    ]
