from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.utils import timezone
from recurrence.fields import RecurrenceField

# Create your models here.


class Events(models.Model):
    event_id = models.CharField(max_length=500, unique=True)
    created = models.DateTimeField(null=True)
    updated = models.DateTimeField(null=True)
    summary = models.CharField(max_length=1000)
    description = models.TextField()
    start_dateTime = models.DateTimeField(null=True)
    end_dateTime = models.DateTimeField(null=True)
    location = models.CharField(max_length=1000,null=True)
    attendees = ArrayField(models.CharField(max_length=500), blank=True,null= True)
    resources_used = ArrayField(models.CharField(max_length=1000), blank=True, default=[])
    event_dump = JSONField(default={})
    creator = models.CharField(max_length=400,blank=True,null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    recurr = RecurrenceField(null=True)
    status = models.TextField(null=True)
    changed_dates = ArrayField(models.DateField(), blank=True, default=[])
    parent_event = models.ForeignKey('self', on_delete=models.CASCADE,null=True,blank=True,to_field='event_id')


class Resources(models.Model):
    resourceUUID = models.CharField(max_length=64, default='')
    resourceName = models.CharField(max_length=30,blank=True)
    resourceEmail = models.CharField(max_length=100,unique= True)
    resourceId = models.CharField(max_length=500)
    generatedResourceName = models.CharField(max_length=100)
    resourceType = models.CharField(max_length=50)
    capacity = models.IntegerField()
    resourceCategory = models.CharField(max_length=20)
    buildingId = models.CharField(max_length=30, blank=True)
    floorName = models.CharField(max_length=30, blank=True)
    resourceDumpdata = JSONField(default={})
    events = models.ManyToManyField(Events, blank=True)
    resourceCreated = models.DateTimeField(default=timezone.now, blank=True)
    roomLoginName = models.CharField(max_length=20,blank=True)
    roomPassword = models.CharField(max_length=20,blank=True)
    roomUrl = models.URLField(blank=True)
    syncToken = models.CharField(max_length=40,blank=True)




