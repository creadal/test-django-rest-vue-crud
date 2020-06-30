from django.db import models

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=200,blank=False, default='')
    date = models.DateTimeField()
    email = models.CharField(max_length=70, blank=False, default='')