from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from MyResources.serializers import EventsSerializer
from MyResources.models import Events
from MyResources.insert import insertEvent,insertResource
from django.contrib.auth.models import User
from rest_framework import generics
from MyResources.serializers import UserSerializer
from rest_framework import permissions
# Create your views here.

class AddEvent(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request , format =None):
        return Response("data entered")

    def post(self, request, format=None):
        #event = Events(summary=request.data['summary'])
        insertEvent(self,request.data['location'], request.data)
        return Response("data entered", status=201)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class AddResource(APIView):
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self,request,format=None):
        return ("reposone returned")

    def post(self,request,format=None):
        insertResource(self,request.data)
        return Response("data entered", status=201)



class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

