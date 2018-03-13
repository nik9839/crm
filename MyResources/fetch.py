from django.db.models import Q, F

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
    stats_dict['booked_now'] = Events.objects.filter(Q(start_dateTime__gte=timezone.now()) | Q(start_date__gt= timezone.datetime.today())).count()
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
        room_dict['hours'] = round(resource_hours(resource_objects[i].events.filter(start_dateTime__gt=resource_objects[i].resourceCreated)),2)
        room_dict['utilization'] = str(round((room_dict['hours'] / resource_present_hours(resource_objects[i])) * 100,
                                         2))+'%'  # problem within the called function
        items.append(room_dict)

    room_wise_dict['list'] = items
    return room_wise_dict


def resource_hours(events):
    total_utilized_time = 0
    for event in events:
        if event.end_dateTime != None:
            diff = event.end_dateTime - event.start_dateTime
        else:
            diff = event.end_date - event.start_date
        days = diff.days
        days_to_hours = days * 8
        diff_btw_two_times = diff.seconds / 3600
        overall_hours = days_to_hours + diff_btw_two_times
        total_utilized_time = total_utilized_time + overall_hours

    return total_utilized_time

def resource_hours2(resource_email):
    abc = Resources.objects.get(resourceEmail=resource_email).events.exclude(start_date__isnull=False).annotate(diff = (F('end_dateTime')- F('start_dateTime'))).first()
    # (diff.days * 8) + (diff.seconds / 3600)
    x = abc.diff


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
        a = resource_objects[i].resourceCreated.date()
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
    resource_obj =Resources.objects.prefetch_related('events').get(resourceEmail=resource_email)
    today_date = timezone.datetime.today()
    try:
        #meetings = resource_obj.events.filter(Q(end_dateTime__date=today_date,start_dateTime__lte=timezone.now())| Q(end_date__gte=today_date,start_date__lte=today_date)).order_by('start_dateTime')
        meetings = resource_obj.events.exclude(recurr__isnull=False).filter(Q(end_dateTime__gte=timezone.now(),end_dateTime__lte=timezone.now() + timedelta(1)) | Q(end_dateTime__gte=timezone.now(),start_dateTime__lte=timezone.now()) |Q(end_date__gt=today_date,start_date__lte=today_date)).order_by('start_dateTime')

    except Exception as e:
        print(e)

    meetings_dict = {}
    items = []

    tz = pytz.timezone('Asia/Kolkata')
    zone = timezone.now().astimezone(tz)

    for meeting in meetings:
        meeting_dict = dict()
        meeting_dict['event_id'] = meeting.event_id
        meeting_dict['summary'] = meeting.summary
        if meeting_dict['summary'] == '':
            meeting_dict['summary'] = 'No title'
        meeting_dict['description'] = meeting.description
        if meeting_dict['description'] == '':
            meeting_dict['description'] = 'No Description'
        meeting_dict['created'] = meeting.created
        meeting_dict['updated'] = meeting.updated
        meeting_dict['attendees'] = meeting.attendees
        meeting_dict['resources_used'] = meeting.resources_used
        meeting_dict['start_dateTime'] = meeting.start_dateTime
        meeting_dict['end_dateTime'] = meeting.end_dateTime
        meeting_dict['location'] = meeting.location
        meeting_dict['creator'] = meeting.creator
        if meeting_dict['start_dateTime']==None:
            meeting_dict['start_dateTime'] = zone.replace(hour=00,minute=00,second=00)
            meeting_dict['end_dateTime'] = zone.replace(hour=23,minute=59,second=59)
        items.append(meeting_dict)


    meetings2= resource_obj.events.filter(recurr__isnull=False)


    for meeting in meetings2:
        try:
            if meeting.recurr.between(datetime.now().replace(hour=0,minute=0,second=0,microsecond=0),datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(1),inc=True)[0] !=None :
                if meeting.start_dateTime != None:
                     a = meeting.end_dateTime.time() > datetime.now().time()
                else:
                    a = True
                if a:
                    meeting_dict = dict()
                    meeting_dict['event_id'] = meeting.event_id
                    meeting_dict['summary'] = meeting.summary
                    if meeting_dict['summary'] == '':
                        meeting_dict['summary'] = 'No title'
                    meeting_dict['description'] = meeting.description
                    if meeting_dict['description'] == '':
                        meeting_dict['description'] = 'No Description'
                    meeting_dict['created'] = meeting.created
                    meeting_dict['updated'] = meeting.updated
                    meeting_dict['attendees'] = meeting.attendees
                    meeting_dict['resources_used'] = meeting.resources_used
                    meeting_dict['start_dateTime'] = meeting.start_dateTime
                    meeting_dict['end_dateTime'] = meeting.end_dateTime
                    if meeting_dict['start_dateTime'] == None:
                        meeting_dict['start_dateTime'] = zone.replace(hour=00, minute=00, second=00)
                        meeting_dict['end_dateTime'] = zone.replace(hour=23, minute=59, second=59)
                    else:
                        time = datetime.now()
                        meeting_dict['start_dateTime'] = meeting.start_dateTime.replace(year=time.year,
                                                                                        month=time.month, day=time.day)
                        meeting_dict['end_dateTime'] = meeting.end_dateTime.replace(year=time.year,
                                                                                    month=time.month, day=time.day)
                        # diff = meeting.end_dateTime.date() - meeting.start_dateTime.date()
                        # if diff == 0:
                        #
                        # else:
                        #     meeting_dict['end_dateTime'] = meeting.end_dateTime.replace(year=time.year,
                        #                                                                 month=time.month,
                        #                                                                 day=time.day + 1)
                    meeting_dict['location'] = meeting.location
                    meeting_dict['creator'] = meeting.creator
                    items.append(meeting_dict)

                    items = sorted(items, key=lambda k: k['start_dateTime'])
        except Exception as e:
            print(e)



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
        rooms_dictionary['calenderName'] = rooms[i].generatedResourceName
        room_dictionary['name'] = rooms[i].roomName
        room_dictionary['password'] = rooms[i].roomPassword
        room_dictionary['capacity'] = rooms[i].capacity
        items.append(room_dictionary)

    rooms_dictionary['items']= items

    return rooms_dictionary

#def generate_autn_token():
