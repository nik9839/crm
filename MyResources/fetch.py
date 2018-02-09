from MyResources.models import Events, Resources
from datetime import datetime

def overallStatsFunction():
    stats_dict = {}
    stats_dict['total_meeting_rooms'] = Resources.objects.count()
    stats_dict['total_events'] = Events.objects.count()
    stats_dict['booked_now'] = Events.objects.filter(start_dateTime__lte=datetime.now()).count()

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
        resource_utilization_hours(resource_objects[i])
        items.append(room_dict)

    room_wise_dict['list']=items
    return room_wise_dict

def resource_utilization_hours(resource_object):
    total_utilized_time = 0
    for i in range(resource_object.events.count()):
        total_utilized_time = total_utilized_time + resource_object.events[i].time_taken # make this field in events model

    #total_time =   current Time - time when resource is added


