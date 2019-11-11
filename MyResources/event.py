import dateutil
import dateutil.parser
import pytz

from MyResources.models import Events, Resources


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
                   description=eventobject.get('description', ''),
                   start_dateTime=eventobject.get('start', {}).get('dateTime', None),
                   end_dateTime=eventobject.get('end', {}).get('dateTime', None),
                   location=eventobject.get('location', None),
                   event_dump=eventobject, attendees=attendees_list, resources_used=resources_used_list,
                   creator=eventobject.get('organizer', {}).get('email', None),
                   start_date=eventobject.get('start', {}).get('date', None),
                   end_date=eventobject.get('end', {}).get('date', None),
                   recurr=eventobject.get('recurrence', [None])[0], status=eventobject.get('status'))

    if eventobject.get('recurringEventId') is not None:
        parent = Events.objects.get(event_id=eventobject.get('recurringEventId'))
        event.parent_event = parent
        if eventobject.get('start', {}).get('dateTime', None) is None:
            parent.changed_dates.append(eventobject.get('start', {}).get('date', None))
        else:
            tz = pytz.timezone('Asia/Kolkata')
            parent.changed_dates.append(
                dateutil.parser.parse(eventobject.get('start', {}).get('dateTime', None)).astimezone(tz).date())
        parent.save()
    event.save()

    for j in range(len(resources_used_list)):
        resource = Resources.objects.get(resourceEmail=resources_used_list[j])
        event_exist = check_if_event_exist_for_that_time(resource, event)
        if not event_exist:
            resource.events.add(event)
            resource.save()


def deleteEvent2(resource_email, eventobject):
    if Events.objects.filter(event_id=eventobject['id']).exists():
        event = Events.objects.get(event_id=eventobject['id'])

        Resources.objects.get(resourceEmail=resource_email).events.remove(event)
        event.resources_used.remove(resource_email)
        event.status = eventobject['status']
        event.save()
        return 'deleted'

    if eventobject.get('recurringEventId', None) is not None:
        parent = Events.objects.get(event_id=eventobject.get('recurringEventId'))
        if eventobject.get('originalStartTime', {}).get('dateTime', None) is None:
            parent.changed_dates.append(eventobject.get('originalStartTime', {}).get('date', None))
        else:
            tz = pytz.timezone('Asia/Kolkata')
            parent.changed_dates.append(
                dateutil.parser.parse(eventobject.get('originalStartTime', {}).get('dateTime', None)).astimezone(
                    tz).date())
        parent.save()


def delete_event(eventobject):
    if Events.objects.filter(event_id=eventobject['id']).exists():
        event = Events.objects.get(event_id=eventobject['id'])
        resources_used = event.resources_used

        for resource in resources_used:
            Resources.objects.get(resourceEmail=resource).events.remove(event)

        event.resources_used = []
        event.status = eventobject['status']
        event.save()
        return 'deleted'

    if eventobject.get('recurringEventId', None) is not None:
        parent = Events.objects.get(event_id=eventobject.get('recurringEventId'))
        if eventobject.get('originalStartTime', {}).get('dateTime', None) is None:
            parent.changed_dates.append(eventobject.get('originalStartTime', {}).get('date', None))
        else:
            tz = pytz.timezone('Asia/Kolkata')
            parent.changed_dates.append(
                dateutil.parser.parse(eventobject.get('originalStartTime', {}).get('dateTime', None)).astimezone(
                    tz).date())
        parent.save()


def check_if_event_exist_for_that_time(resource, event):
    from django.db.models import Q
    event_start = event.start_dateTime
    event_end = event.end_dateTime

    meetings_normal = 0
    meetings_recurr = 0
    try:
        meetings_normal = resource.events.exclude(recurr__isnull=False).filter(
            Q(end_dateTime__gte=event_start, end_dateTime__lte=event_end) | Q(end_dateTime__gte=event_start,
                                                                              start_dateTime__lte=event_start) | Q(
                start_dateTime__gte=event_start, start_dateTime__lte=event_end, end_dateTime__gte=event_end)).count()
    except Exception as e:
        print(e)


    try:
        mmm = event_start.date()
        local_tz = pytz.timezone('Asia/Kolkata')
        meetings_recurr = resource.events.filter(recurr__isnull=False)
        filtered_meetings = meetings_recurr.exclude(changed_dates__contains=[mmm])
        for meeting in filtered_meetings:
            zzz = meeting.recurr.between(event_start, event_end,
                                         dtstart=meeting.start_dateTime.astimezone(local_tz).replace(hour=0, minute=0,
                                                                                                     second=0,
                                                                                                     microsecond=0,
                                                                                                     tzinfo=None),
                                         inc=True)
            if len(zzz) > 0:
                if meeting.start_dateTime != None:
                    a = meeting.end_dateTime.time() > event_start.time()
                else:
                    a = True
                if a:
                    meetings_recurr = 1
                    break
    except Exception as e:
        print(e)

    total_meetings = meetings_normal + meetings_recurr
    print(total_meetings)
    if total_meetings:
        return True
    else:
        return False
