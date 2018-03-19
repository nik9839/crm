from django.db.models import Q, F, Func, Case, When, IntegerField, Sum, Count
from django.db.models.functions import Extract

from MyResources.models import Events, Resources
from datetime import datetime, timedelta
from django.utils import timezone
import pytz
import jwt
from pg_utils import Seconds
import dateutil.parser



def overallStatsFunction(sDate,eDate,searchQuery):
    local_tz = pytz.timezone('Asia/Kolkata')
    stats_dict = dict()
    stats_dict['total_meeting_rooms'] = Resources.objects.filter(generatedResourceName__icontains=searchQuery).count()
    stats_dict['total_events'] = Events.objects.filter(resources_used__len__gt= 0).filter(Q(start_dateTime__gte=sDate , end_dateTime__lte=eDate) | Q(start_date__gte=dateutil.parser.parse(sDate).astimezone(local_tz).date(), end_date__lte=dateutil.parser.parse(eDate).astimezone(local_tz).date())).count()
    stats_dict['booked_now'] = Events.objects.filter(Q(start_dateTime__gte=timezone.now()) | Q(start_date__gt= timezone.datetime.today())).count()
    stats_dict['utilization'], stats_dict['hours'] = overallUtilization(sDate,eDate,searchQuery)
    return stats_dict


def room_wise_stats(sDate,eDate,text):
    room_wise_dict = {}
    items = []
    # if len(locations)== 0:
    #     resource_objects = Resources.objects.all()
    # else:
    #     resource_objects = Resources.objects.filter(buildingId__in=locations)


    resource_objects = Resources.objects.filter(Q(generatedResourceName__icontains=text))
    local_tz = pytz.timezone('Asia/Kolkata')

    resorce_present = resource_present_hours(sDate,eDate)
    for i in range(resource_objects.count()):
        room_dict = dict()
        room_dict['email'] = resource_objects[i].resourceEmail
        room_dict['room_name'] = resource_objects[i].resourceName
        room_dict['calender_name'] = resource_objects[i].generatedResourceName
        room_dict['location'] = resource_objects[i].buildingId
        room_dict['meetings'] = resource_objects[i].events.filter(Q(start_dateTime__gte=sDate , end_dateTime__lte=eDate) | Q(start_date__gte=dateutil.parser.parse(sDate).astimezone(local_tz).date(), end_date__lte=dateutil.parser.parse(eDate).astimezone(local_tz).date())).count()
        room_dict['capacity'] = resource_objects[i].capacity
        room_dict['hours'] = resource_hours2(resource_objects[i].resourceEmail,sDate,eDate)
        room_dict['utilization'] = str(round((room_dict['hours'] / resorce_present) * 100,
                                         2))+'%'
        room_dict['floor']= resource_objects[i].floorName
        #room_dict['space_utlization']= resource_space_utilzation(sDate,eDate,resource_objects[i].resourceEmail)
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

def resource_space_utilzation(sDate,eDate,resource):
    print(Resources.objects.get(resourceEmail=resource).resourceName)
    local_tz = pytz.timezone('Asia/Kolkata')
    total_possible_capacity = Resources.objects.get(resourceEmail=resource).events.count() * int(Resources.objects.get(resourceEmail=resource).capacity)
    if total_possible_capacity ==0:
        return 0
    total_attendees = Resources.objects.get(resourceEmail=resource).events\
        .filter(Q(start_dateTime__gte=sDate , end_dateTime__lte=eDate) | Q(start_date__gte=dateutil.parser.parse(sDate)
                                                                           .astimezone(local_tz).date(), end_date__lte=dateutil.parser.parse(eDate)
                                                                           .astimezone(local_tz).date())).annotate(ac=Count('attendees')).aggregate(resource_attendees= Sum('ac')).get('resource_attendees',0)
    if total_attendees == None:
        total_attendees=0
    return round(total_attendees/total_possible_capacity,2)



def resource_hours2(resource_email,sDate,eDate):
    local_tz = pytz.timezone('Asia/Kolkata')
    total_time =  Resources.objects.get(resourceEmail=resource_email).events.filter(Q(start_dateTime__gte=sDate , end_dateTime__lte=eDate) | Q(start_date__gte=dateutil.parser.parse(sDate).astimezone(local_tz).date(), end_date__lte=dateutil.parser.parse(eDate).astimezone(local_tz).date())).aggregate( time = Sum(Case(
            When(start_date__isnull=True,
                 then=Seconds(F('end_dateTime') - F('start_dateTime'))
                 ),
            When(start_date__isnull=False,
                 then=Extract((Func(F('end_date'), F('start_date'), function='age')), 'day') * 8 * 3600
                 ),
            output_field=IntegerField()
            ),
    )).get('time',0)

    if total_time is None:
        total_time=0
    else:
        total_time=round(total_time/3600,2)
    return total_time

def resource_present_hours(sDate,eDate):
    diff = dateutil.parser.parse(eDate) - dateutil.parser.parse(sDate)
    days = diff.days
    days_to_hours = days * 24  # assuming 8 workings hours a day
    diff_btw_two_times = diff.seconds / 3600
    overall_hours = days_to_hours + diff_btw_two_times

    return overall_hours



def overallUtilization(sDate,eDate,text):
    total_hours_resources_present = 0
    total_hours_resource_utilized = 0
    resource_objects = Resources.objects.filter(Q(generatedResourceName__icontains=text))

    resource_present = resource_present_hours(sDate,eDate)
    for i in range(resource_objects.count()):
        total_hours_resources_present = total_hours_resources_present + resource_present
        total_hours_resource_utilized = total_hours_resource_utilized + resource_hours2(resource_objects[i].resourceEmail,sDate,eDate)

    return round((total_hours_resource_utilized / total_hours_resources_present) * 100,2),total_hours_resource_utilized


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
        local_tz = pytz.timezone('Asia/Kolkata')
        dt=timezone.now().astimezone(local_tz).replace(hour=23,minute=59,second=59)
        meetings = resource_obj.events.exclude(recurr__isnull=False).filter(Q(end_dateTime__gte=timezone.now(),end_dateTime__lte=dt) | Q(end_dateTime__gte=timezone.now(),start_dateTime__lte=timezone.now()) | Q(start_dateTime__gte= timezone.now(), start_dateTime__lte= dt,end_dateTime__gte= dt) | Q(end_date__gt=today_date,start_date__lte=today_date)).order_by('start_dateTime')

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
        room_dictionary['calenderName'] = rooms[i].generatedResourceName
        room_dictionary['name'] = rooms[i].resourceName
        room_dictionary['username'] = rooms[i].roomLoginName
        room_dictionary['password'] = rooms[i].roomPassword
        room_dictionary['capacity'] = rooms[i].capacity
        items.append(room_dictionary)

    rooms_dictionary['items']= items

    return rooms_dictionary

