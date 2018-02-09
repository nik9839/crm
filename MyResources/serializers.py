from rest_framework import serializers
from MyResources.models import Resources , Events
from django.contrib.auth.models import User

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ('id', 'summary', 'description', 'start_dateTime', 'end_datTime', 'location')

    def validate(self, attrs):
        import ipdb; ipdb.set_trace()
        print(attrs)



class ResourceSerializer(serializers.ModelSerializer):
        # owner = serializers.HyperlinkedRelatedField(default=User.objects.all()[0])
        class Meta:
            model = Resources
            fields =('id','resourceId','resourceName','generatedResourceName','resourceType','resourceEmail','capacity','resourceCategory','events')


class UserSerializer(serializers.ModelSerializer):
    events = serializers.PrimaryKeyRelatedField(many=True, queryset=Events.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'events')