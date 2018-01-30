from rest_framework import serializers
from MyResources.models import Resources , Events
from django.contrib.auth.models import User

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ('id','summary', 'description', 'start_dateTime', 'end_datTime', 'location','owner','highlighted')
        owner = serializers.ReadOnlyField(source='owner.username')


class ResourceSerializer(serializers.ModelSerializer):
        class Meta:
            model = Resources
            fields =('id','resourceId','resourceName','generatedResourceName','resourceType','resourceEmail','capacity','resourceCategory','events','owner','highlighted');



class UserSerializer(serializers.ModelSerializer):
    events = serializers.PrimaryKeyRelatedField(many=True, queryset=Events.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'events')