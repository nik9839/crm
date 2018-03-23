import dateutil
from MyResources.models import Events, Resources
import pytz
import dateutil.parser


def insertEvent(resource_email, eventobject):
    if Events.objects.filter(event_id=eventobject['id']).exists():
        obj = Events.objects.get(event_id=eventobject['id'])
        resources_present_list = obj.resources_used
        for j in range(len(resources_present_list)):
            resource = Resources.objects.get(resourceEmail=resources_present_list[j])
            resource.events.remove(obj)
        Events.objects.filter(event_id=eventobject['id']).delete()

    attendees_list = []
    resources_used_list = []

    # check if no attendees field
    if eventobject.get('attendees', None) is None:
        eventobject['attendees'] = []

    if eventobject.get('start', {}).get('dateTime', None) is None:
        local_tz = pytz.timezone('Asia/Kolkata')
        sDate = eventobject.get('start', {}).get('date', None)
        eDate = eventobject.get('end', {}).get('date', None)
        eventobject['start']['dateTime'] = str(
            dateutil.parser.parse(sDate).astimezone(local_tz).replace(hour=00, minute=00, second=00))
        eventobject['end']['dateTime'] = str(
            dateutil.parser.parse(eDate).astimezone(local_tz).replace(hour=00, minute=00, second=00))

    for i in range(len(eventobject['attendees'])):
        if not (eventobject['attendees'][i].get('resource')):
            attendees_list.append(eventobject['attendees'][i]['email'])
        else:
            if eventobject['attendees'][i]['responseStatus'] != "declined":
                resources_used_list.append(eventobject['attendees'][i]['email'])
    event = Events(event_id=eventobject['id'], created=eventobject.get('created'), updated=eventobject.get('updated'),
                   summary=eventobject.get('summary', ''),
                   description=eventobject.get('description', ''), start_dateTime=eventobject.get('start',{}).get('dateTime',None),
                   end_dateTime=eventobject.get('end',{}).get('dateTime', None), location=eventobject.get('location',None),
                   event_dump=eventobject, attendees=attendees_list, resources_used=resources_used_list,
                   creator=eventobject.get('creator',{}).get('email',None), start_date= eventobject.get('start',{}).get('date',None),
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
        event.save()


