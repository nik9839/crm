from rest_framework.views import APIView
from rest_framework.response import Response
from MyResources.insert import insertEvent,insertResource
from MyResources.models import Resources
from django.http import HttpResponse
from MyResources.fetchCalenderData import *
import requests
from MyResources.fetch import *

# Create your views here.


@api_view(['GET', 'POST'])
def notify(request):
    try:
        uuid = request._request.META['HTTP_X_GOOG_CHANNEL_ID']
        resource_email = Resources.objects.get(resourceUUID=uuid).resourceEmail
        test_api_request(resource_email)
        return HttpResponse('data inserted')
    except Exception:
        print("exception occured")

class AddResource(APIView):
    def post(self,request,format=None):
        insertResource(self,request.data)
        return Response("data entered")


def test(request):
    return HttpResponse(print_index_table())

class OverallStats(APIView):
    def get(self,request,format=None):
        return Response(overallStatsFunction())

class RoomStats(APIView):
    def get(self,request,format=None):
        return Response(room_wise_stats())



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

