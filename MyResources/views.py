from rest_framework.decorators import api_view
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.response import Response
from MyResources.resources import insertResource
from MyResources.fetchCalenderData import *
from MyResources.fetch import *


# Create your views here.


# Issue of multiple notification for same change
@api_view(['GET', 'POST'])
def notify(request):
    try:
        if not request._request.META['HTTP_X_GOOG_RESOURCE_STATE'] == 'sync':
            uuid = request._request.META['HTTP_X_GOOG_CHANNEL_ID']
            #print(request._request.META['HTTP_X_GOOG_RESOURCE_STATE'])
            resource_email = Resources.objects.get(resourceUUID=uuid).resourceEmail
            get_changes(resource_email)
        return Response(status=HTTP_202_ACCEPTED)
    except Exception:
        return Response(status=HTTP_202_ACCEPTED)


class AddResource(APIView):
    def post(self, request):
        insertResource(self, request.data)
        return Response("data entered")


def test(request):
    return HttpResponse(print_index_table())


class OverallStats(APIView):
    def get(self, request):
        return Response(overallStatsFunction(), status=HTTP_202_ACCEPTED)


class RoomStats(APIView):
    def get(self, request):
        return Response(room_wise_stats(), status=HTTP_202_ACCEPTED)


class Meetings(APIView):
    def post(self, request):
        return Response(getMeetings(request.data['items'], status=HTTP_202_ACCEPTED))


class RoomMeetings(APIView):
    def post(self, request):
        return Response(getMeetingsOfRoomOfaDay(request.data['email_id']), status=HTTP_202_ACCEPTED)


class CheckLogin(APIView):
    def post(self, request):
        return Response(checkCredentials(request.data), status=HTTP_202_ACCEPTED)


class RoomDetails(APIView):
    def get(self, request):
        return Response(room_details(), status=HTTP_202_ACCEPTED)
