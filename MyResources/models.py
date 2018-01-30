from django.db import models
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

# Create your models here.
class Events(models.Model):
    summary = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    start_dateTime = models.CharField(max_length=50)
    end_datTime = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', related_name='events', on_delete=models.CASCADE)
    highlighted = models.TextField()

class Resources(models.Model):
    resourceId = models.CharField(max_length=500, null=True)
    resourceName = models.CharField(max_length=50)
    generatedResourceName = models.CharField(max_length=100)
    resourceType = models.CharField(max_length=10)
    resourceEmail = models.CharField(max_length=100)
    capacity = models.IntegerField()
    resourceCategory = models.CharField(max_length=20)
    events = models.ManyToManyField(Events,blank=True)
    owner = models.ForeignKey('auth.User', related_name='resource', on_delete=models.CASCADE)
    highlighted = models.TextField()
    #buildingId = models.CharField(max_length=10)
    #floorName = models.CharField(max_length=10)
    #features


