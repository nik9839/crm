from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.response import Response
from MyResources.insert import insertResource
from MyResources.fetchCalenderData import *
from MyResources.fetch import *

# Create your views here.


@api_view(['GET', 'POST'])
def notify(request):
    try:
        uuid = request._request.META['HTTP_X_GOOG_CHANNEL_ID']
        resource_email = Resources.objects.get(resourceUUID=uuid).resourceEmail
        get_data_from_calender(resource_email)
        return Response('data inserted', status=HTTP_202_ACCEPTED)
    except Exception:
        return Response('data inserted', status=HTTP_202_ACCEPTED)


class AddResource(APIView):
    def post(self, request):
        insertResource(self,request.data)
        return Response("data entered")


def test(request):
    return HttpResponse(print_index_table())


class OverallStats(APIView):
    def get(self, request):
        return Response(overallStatsFunction())


class RoomStats(APIView):
    def get(self,request):
        return Response(room_wise_stats())


class Meetings(APIView):
    def post(self, request):
        return Response(getMeetings(request.data['items']))


class RoomMeetings(APIView):
    def post(self, request):
     return Response(getMeetingsOfRoomOfaDay(request.data['email_id']))


class CheckLogin(APIView):
    def post(self,request):
        return Response(checkCredentials(request.data))

class RoomDetails(APIView):
    def get(self,request):
        return Response(room_details())
