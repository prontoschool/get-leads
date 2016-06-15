from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Contact(models.Model):
    #firstname = models.CharField(max_length=200)
    #lastname = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    email = models.EmailField(default='')
    ip = models.CharField(max_length=200)

