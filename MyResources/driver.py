from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from MyResources.serializers import EventsSerializer
from MyResources.models import Events


event = Events(summary="My Event",description="His djbj",start_dateTime="2018-01-29T10:19:32.663Z",end_datTime="2018-01-29T10:19:32.663Z",location="gurgoan")