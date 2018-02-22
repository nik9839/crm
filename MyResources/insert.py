import uuid

from MyResources.models import Events, Resources

def insertEvent(resource_email,eventobject):
    attendees_list = []
    resources_used_list = []

    for i in range(len(eventobject['attendees'])):
        if not (eventobject['attendees'][i].get('resource')):
            attendees_list.append(eventobject['attendees'][i]['email'])
        else:
            resources_used_list.append(eventobject['attendees'][i]['email'])

    event = Events(event_id=eventobject['id'], created=eventobject['created'], updated=eventobject['updated'],
                   summary=eventobject['summary'],
                   description=eventobject.get('description', ''), start_dateTime=eventobject['start']['dateTime'],
                   end_dateTime=eventobject['end']['dateTime'], location=eventobject['location'],
                   event_dump=eventobject, attendees=attendees_list, resources_used=resources_used_list)

    if Events.objects.filter(event_id=eventobject['id']).exists():
        obj = Events.objects.get(event_id=eventobject['id'])
        for j in range(len(resources_used_list)):
            resource = Resources.objects.get(resourceEmail=resources_used_list[j])
            resource.events.remove(obj)
        Events.objects.filter(event_id=eventobject['id']).delete()

    event.save()
    for j in range(len(resources_used_list)):
        resource = Resources.objects.get(resourceEmail=resources_used_list[j])
        resource.events.add(event)
        resource.save()


def deleteEvent(eventobject):
    if Events.objects.filter(event_id=eventobject['id']).exists():
        resources_used_list = []
        for i in range(len(eventobject['attendees'])):
            if eventobject['attendees'][i].get('resource'):
                resources_used_list.append(eventobject['attendees'][i]['email'])

        obj = Events.objects.get(event_id=eventobject['id'])

        for j in range(len(resources_used_list)):
            resource = Resources.objects.get(resourceEmail=resources_used_list[j])
            resource.events.remove(obj)

        Events.objects.filter(event_id=eventobject['id']).delete()

def insertResource(self,resourceObject):

    if resourceObject.get('capacity')==None:
        resourceObject['capacity']=0

    if resourceObject.get('buildingId')==None:
        resourceObject['buildingId']='---'
        resourceObject['floorName'] = 0

    resource = Resources(resourceEmail=resourceObject['resourceEmail'],resourceId=resourceObject['resourceId'],
                         generatedResourceName=resourceObject['generatedResourceName'],resourceType=resourceObject['resourceType'],
                         capacity=resourceObject['capacity'],resourceCategory=resourceObject['resourceCategory'],
                         buildingId=resourceObject['buildingId'],floorName=resourceObject['floorName'], resourceDumpdata=resourceObject,
                         resourceUUID= uuid.uuid4())
    resource.save()
