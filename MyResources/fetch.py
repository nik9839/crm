from MyResources.models import Events, Resources
from datetime import datetime, timedelta, time
from django.utils import timezone
import pytz
import jwt
# utc = pytz.UTC


def overallStatsFunction():
    stats_dict = dict()
    stats_dict['total_meeting_rooms'] = Resources.objects.count()
    stats_dict['total_events'] = Events.objects.count()
    stats_dict['booked_now'] = Events.objects.filter(start_dateTime__gte=timezone.now()).count()
    stats_dict['utilization'] = round(overallUtilization(), 2)
    return stats_dict


def room_wise_stats():
    room_wise_dict = {}
    items = []
    resource_objects = Resources.objects.all()

    for i in range(resource_objects.count()):
        room_dict = dict()
        room_dict['email'] = resource_objects[i].resourceEmail
        room_dict['room_name'] = resource_objects[i].resourceName
        room_dict['calender_name'] = resource_objects[i].generatedResourceName
        room_dict['location'] = resource_objects[i].buildingId
        room_dict['meetings'] = resource_objects[i].events.count()
        room_dict['capacity'] = resource_objects[i].capacity
        room_dict['hours'] = round(resource_hours(resource_objects[i].events.all()),2)
        room_dict['utilization'] = str(round((room_dict['hours'] / resource_present_hours(resource_objects[i])) * 100,
                                         2))+'%'  # problem within the called function
        items.append(room_dict)

    room_wise_dict['list'] = items
    return room_wise_dict


def resource_hours(events):
    total_utilized_time = 0
    for event in events:
        diff = event.end_dateTime - event.start_dateTime
        days = diff.days
        days_to_hours = days * 8
        diff_btw_two_times = diff.seconds / 3600
        overall_hours = days_to_hours + diff_btw_two_times
        total_utilized_time = total_utilized_time + overall_hours

    return total_utilized_time


def resource_present_hours(resource):
    created = resource.resourceCreated
    now = timezone.now()
    diff = now - created  # problem in calculating diff due to conflicting timeZone offsets
    days = diff.days
    days_to_hours = days * 8  # assuming 8 workings hours a day
    diff_btw_two_times = diff.seconds / 3600
    overall_hours = days_to_hours + diff_btw_two_times

    return overall_hours


def overallUtilization():
    total_hours_resources_present = 0
    total_hours_resource_utilized = 0
    resource_objects = Resources.objects.all()

    for i in range(resource_objects.count()):
        total_hours_resources_present = total_hours_resources_present + resource_present_hours(resource_objects[i])
        total_hours_resource_utilized = total_hours_resource_utilized + resource_hours(resource_objects[i].events.all())

    return (total_hours_resource_utilized / total_hours_resources_present) * 100


def getMeetings(resources_list):
    all_meetings_dict = {}
    items = []

    meetings = Events.objects.filter(resources_used__overlap=resources_list).all()
    for meeting in meetings:
        meeting_dict = dict()
        meeting_dict['event_id'] = meeting.event_id
        meeting_dict['summary'] = meeting.summary
        meeting_dict['description'] = meeting.description
        meeting_dict['created'] = meeting.created
        meeting_dict['updated'] = meeting.updated
        meeting_dict['attendees'] = meeting.attendees
        meeting_dict['resources_used'] = meeting.resources_used
        meeting_dict['start_dateTime'] = meeting.start_dateTime
        meeting_dict['end_dateTime'] = meeting.end_dateTime
        meeting_dict['location'] = meeting.location
        items.append(meeting_dict)

    all_meetings_dict['items'] = items
    return all_meetings_dict


def getMeetingsOfRoomOfaDay(resource_email):
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_end = datetime.combine(tomorrow, time())
    resource_obj =Resources.objects.prefetch_related('events').get(resourceEmail=resource_email)
    meetings = resource_obj.events.filter(end_dateTime__date=timezone.datetime.today())\
        .filter(start_dateTime__gte=timezone.now()).order_by('start_dateTime')

    meetings_dict = {}
    items = []

    for meeting in meetings:
        meeting_dict = dict()
        meeting_dict['event_id'] = meeting.event_id
        meeting_dict['summary'] = meeting.summary
        meeting_dict['description'] = meeting.description
        meeting_dict['created'] = meeting.created
        meeting_dict['updated'] = meeting.updated
        meeting_dict['attendees'] = meeting.attendees
        meeting_dict['resources_used'] = meeting.resources_used
        meeting_dict['start_dateTime'] = meeting.start_dateTime
        meeting_dict['end_dateTime'] = meeting.end_dateTime
        meeting_dict['location'] = meeting.location
        meeting_dict['creator'] = meeting.creator
        items.append(meeting_dict)

    meetings_dict['items'] = items
    return meetings_dict


def checkCredentials(data):
    response = dict()
    response['credentials_valid'] = False
    if Resources.objects.filter(roomLoginName__iexact=data['username']).exists():
        resource = Resources.objects.get(roomLoginName__iexact=data['username'])
        if resource.roomPassword == data['password']:
            response['credentials_valid'] = True
            response['capacity'] = resource.capacity
            response['room_name'] = resource.resourceName
            response['room_url'] = resource.roomUrl
            response['token'] = jwt.encode({'email': resource.resourceEmail}, 'secret', algorithm='HS256')
        else:
            response['message'] = "password doesn't match"
    else:
        response['message'] = "room doesn't exist"
    return response


def room_details():
    rooms_dictionary = dict()
    items =[]

    rooms = Resources.objects.all()

    for i in range(len(rooms)):
        room_dictionary = dict()
        room_dictionary['name'] = rooms[i].roomName
        room_dictionary['password'] = rooms[i].roomPassword
        room_dictionary['capacity'] = rooms[i].capacity
        items.append(room_dictionary)

    rooms_dictionary['items']= items

    return rooms_dictionary

#def generate_autn_token():
