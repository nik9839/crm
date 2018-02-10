from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from datetime import datetime, tzinfo
from django.utils import timezone

# Create your models here.

class Events(models.Model):
    event_id = models.CharField(max_length=40)
    created = models.CharField(max_length=30)
    updated = models.CharField(max_length=30)
    summary = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    start_dateTime = models.DateTimeField()
    end_dateTime = models.DateTimeField()
    location = models.CharField(max_length=100)
    attendees = ArrayField(models.CharField(max_length=50), blank=True,null= True)
    event_dump = JSONField(default={})



class Resources(models.Model):
    resourceUUID = models.CharField(max_length=64, default='')
    resourceEmail = models.CharField(max_length=100)
    resourceId = models.CharField(max_length=500)
    generatedResourceName = models.CharField(max_length=100)
    resourceType = models.CharField(max_length=20)
    capacity = models.IntegerField()
    resourceCategory = models.CharField(max_length=20)
    buildingId = models.CharField(max_length=20, blank=True)
    floorName = models.IntegerField(blank=True)
    resourceDumpdata = JSONField(default={})
    events = models.ManyToManyField(Events, blank=True)
    resourceCreated = models.DateTimeField(default=timezone.now, blank=True)




