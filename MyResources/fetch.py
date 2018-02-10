from MyResources.models import Events, Resources
from datetime import datetime
import pytz

utc = pytz.UTC
def overallStatsFunction():
    stats_dict = {}
    stats_dict['total_meeting_rooms'] = Resources.objects.count()
    stats_dict['total_events'] = Events.objects.count()
    stats_dict['booked_now'] = Events.objects.filter(start_dateTime__gte=utc.localize(datetime.now())).count()
    #the above line code for booked now might not working properly may be due to timeZone Problem utc localize is used to change to common format
    stats_dict['utilization'] = overallUtilization()
    return stats_dict


def room_wise_stats():
    room_wise_dict = {}
    items=[]
    resource_objects = Resources.objects.all()

    for i in range(resource_objects.count()):
        room_dict = dict()
        room_dict['name'] = resource_objects[i].generatedResourceName
        room_dict['location'] = resource_objects[i].buildingId
        room_dict['meetings'] = resource_objects[i].events.count()
        room_dict['capacity'] = resource_objects[i].capacity
        room_dict['hours'] = resource_hours(resource_objects[i].events.all())
        room_dict['utilization']= (room_dict['hours']/resource_present_hours(resource_objects[i]))*100  # problem within the called function
        items.append(room_dict)

    room_wise_dict['list'] = items
    return room_wise_dict

def resource_hours(events):
    total_utilized_time = 0
    for event in events:
        diff = event.end_dateTime - event.start_dateTime
        days = diff.days
        days_to_hours = days * 24
        diff_btw_two_times = diff.seconds / 3600
        overall_hours = days_to_hours + diff_btw_two_times
        total_utilized_time = total_utilized_time+overall_hours

    return total_utilized_time


def resource_present_hours(resource):
    created = resource.resourceCreated
    now = utc.localize(datetime.now())
    diff = now-created  # problem in calculating diff due to conflicting timeZone offsets
    days = diff.days
    days_to_hours = days * 8  # assuming 8 workings hours a day
    diff_btw_two_times = diff.seconds / 3600
    overall_hours = days_to_hours + diff_btw_two_times

    return overall_hours

def overallUtilization():
    total_hours_resources_present =0
    total_hours_resource_utilized =0
    resource_objects = Resources.objects.all()

    for i in range(resource_objects.count()):
        total_hours_resources_present = total_hours_resources_present + resource_present_hours(resource_objects[i])
        total_hours_resource_utilized = total_hours_resource_utilized + resource_hours(resource_objects[i].events.all())

    return  (total_hours_resource_utilized/total_hours_resources_present)*100