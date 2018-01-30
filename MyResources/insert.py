from MyResources.models import Events , Resources
from django.contrib.auth.models import User

def insertEvent(self,location,eventobject):
    resource = Resources.objects.all().get(generatedResourceName=location)
    event = Events(summary=eventobject['summary'],description=eventobject['description'],start_dateTime=eventobject['start']['dateTime'],end_datTime=eventobject['end']['dateTime'],location=eventobject['location'],owner=User.objects.all()[0])
    event.save()
    resource.events.add(event)
    resource.save()



def insertResource(self,resourceObject):
    resource = Resources(resourceId=resourceObject['resourceId'],resourceName=resourceObject['resourceName'],generatedResourceName=resourceObject['generatedResourceName'],resourceType=resourceObject['resourceType'],resourceEmail=resourceObject['resourceEmail'],capacity=resourceObject['capacity'],resourceCategory=resourceObject['resourceCategory'],owner=User.objects.all()[0])
    resource.save()