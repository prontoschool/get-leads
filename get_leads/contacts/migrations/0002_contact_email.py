# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-13 07:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='email',
            field=models.EmailField(default='exit', max_length=254),
            preserve_default=False,
        ),
    ]
