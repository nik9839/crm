from MyResources.models import Events, Resources

def insertEvent(resource_email,eventobject):
    if Events.objects.filter(event_id=eventobject['id']).exists():
        obj = Events.objects.get(event_id=eventobject['id'])
        resources_present_list = obj.resources_used
        for j in range(len(resources_present_list)):
            resource = Resources.objects.get(resourceEmail=resources_present_list[j])
            resource.events.remove(obj)
        Events.objects.filter(event_id=eventobject['id']).delete()

    attendees_list = []
    resources_used_list = []

    for i in range(len(eventobject['attendees'])):
        if not (eventobject['attendees'][i].get('resource')):
            attendees_list.append(eventobject['attendees'][i]['email'])
        else:
            if eventobject['attendees'][i]['responseStatus'] != "declined":
                resources_used_list.append(eventobject['attendees'][i]['email'])
    event = Events(event_id=eventobject['id'], created=eventobject['created'], updated=eventobject['updated'],
                   summary=eventobject.get('summary', ''),
                   description=eventobject.get('description', ''), start_dateTime=eventobject.get('start',{}).get('dateTime',None),
                   end_dateTime=eventobject.get('end',{}).get('dateTime', None), location=eventobject.get('location',None),
                   event_dump=eventobject, attendees=attendees_list, resources_used=resources_used_list,
                   creator=eventobject['creator']['email'], start_date= eventobject.get('start',{}).get('date',None),
                   end_date=eventobject.get('end',{}).get('date', None),
                   recurr= eventobject.get('recurrence',[None])[0])

    event.save()
    for j in range(len(resources_used_list)):
        resource = Resources.objects.get(resourceEmail=resources_used_list[j])
        resource.events.add(event)
        resource.save()




def deleteEvent2(resource_email,eventobject):
    if Events.objects.filter(event_id=eventobject['id']).exists():
        event = Events.objects.get(event_id=eventobject['id'])

        Resources.objects.get(resourceEmail=resource_email).events.remove(event)
        event.resources_used.remove(resource_email)

        if len(event.resources_used) == 0:
            event.delete()

