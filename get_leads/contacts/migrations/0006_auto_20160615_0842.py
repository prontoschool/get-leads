# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-15 08:42
from __future__ import unicode_literals

from django.db import migrations, models


def combine_names(apps, schema_editor):
    Contact = apps.get_model('contacts', 'Contact')
    for contact in Contact.objects.all():
        contact.name = "%s %s" % (contact.firstname, contact.lastname)
        contact.save()


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('contacts', '0005_contact_name'),
    ]

    operations = [
        migrations.RunPython(combine_names),
    ]
