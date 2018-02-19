from django.shortcuts import render
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from MyResources.insert import insertResource
from MyResources.fetchCalenderData import *
from MyResources.fetch import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


@api_view(['GET', 'POST'])
def notify(request):
    try:
        uuid = request._request.META['HTTP_X_GOOG_CHANNEL_ID']
        resource_email = Resources.objects.get(resourceUUID=uuid).resourceEmail
        test_api_request(resource_email)
        return Response('data inserted')
    except Exception:
        print("exception occurred")


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

# @api_view(['GET'])
# @renderer_classes((JSONRenderer,))
# def getMeetings2(request):
#     meetings = Events.objects.all()
#     paginator = Paginator(meetings, 2)
#     page = request.GET.get('page')
#     meetings_to_show = paginator.get_page(page)
#     return Response(meetings_to_show)
#     #return Response(meetings_to_show)

# class AddEvent(APIView):
#
#     def get(self, request , format =None):
#         return Response("data entered")
#
#     def post(self, request, format=None):
#         #event = Events(summary=request.data['summary'])
#         insertEvent(self,request.data['location'], request.data)
#         return Response("data entered", status=201)
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)


# class UserList(generics.ListAPIView):
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
# class AddResource2(viewsets.ModelViewSet):
#     serializer_class =ResourceSerializer
#     queryset = Events.objects.all()
#     #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#     def perform_create(self, serializer):
#         # return serializer.save(owner=self.request.user)
#         return serializer.save(owner=User.objects.all()[0])
#
# class AddEvent2(viewsets.ModelViewSet):
#     serializer_class =EventsSerializer
#     queryset = Events.objects.all()
#     #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#     def perform_create(self, serializer):
#         # return serializer.save(owner=self.request.user)
#         return serializer.save(owner=User.objects.all()[0], end_datTime=self.request.data['end']['dateTime'])

