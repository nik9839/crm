import uuid

from rest_framework.decorators import api_view
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.response import Response
from MyResources.resources import insertResource
from MyResources.fetchCalenderData import *
from MyResources.fetch import *
import string
import random

# Create your views here.

user_name = 'xuqnlt'
dashboard_password = '2709288'


# Issue of multiple notification for same change
@api_view(['GET', 'POST'])
def notify(request):
    if not request._request.META['HTTP_X_GOOG_RESOURCE_STATE'] == 'sync':
        uuid = request._request.META['HTTP_X_GOOG_CHANNEL_ID']
        # print(request._request.META['HTTP_X_GOOG_RESOURCE_STATE'])
        resource_email = Resources.objects.get(resourceUUID=uuid).resourceEmail
        get_changes(resource_email)
    return Response(status=HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
def dashboard_login(request):
    response = dict()
    response['isValid'] = False
    if user_name == request.data['username'] and dashboard_password == request.data['password']:
        response['isValid'] = True
        response[
            'imageUrl'] = 'https://indiasmosttrustedcompaniesawards.com/wp-content/uploads/2017/09/DB-Corp-Ltd.Dainik-Bhaskar-Group.jpg'
        return Response(response, status=HTTP_202_ACCEPTED)
    else:
        return Response(response, status=HTTP_202_ACCEPTED)


class AddResource(APIView):
    def post(self, request):
        insertResource(self, request.data)
        return Response("data entered")


class AddMutlipleResources(APIView):
    def post(self, request):
        for resource in request.data['items']:
            insertResource(self, resource)
        return Response("data entered")


def test(request):
    return HttpResponse(print_index_table(request))


class OverallStats(APIView):
    def post(self, request):
        local_tz = pytz.timezone('Asia/Kolkata')
        sDate = request.data['sDate']
        eDate = request.data['eDate']
        try:
            query = request.data['searchQuery']
        except Exception:
            query = ''

        if request.data['sDate'] == '':
            sDate = str(Resources.objects.all()[0].resourceCreated)
        if request.data['eDate'] == '':
            eDate = str(timezone.now().astimezone(local_tz).replace(hour=23, minute=59, second=59))

        return Response(overallStatsFunction(sDate, eDate, query),
                        status=HTTP_202_ACCEPTED)


class RoomStats(APIView):
    def post(self, request):
        local_tz = pytz.timezone('Asia/Kolkata')
        sDate = request.data['sDate']
        eDate = request.data['eDate']
        try:
            query = request.data['searchQuery']
        except Exception:
            query = ''

        if request.data['sDate'] == '':
            sDate = str(Resources.objects.all()[0].resourceCreated)

        if request.data['eDate'] == '':
            eDate = str(timezone.now().astimezone(local_tz).replace(hour=23, minute=59, second=59))

        return Response(room_stats(sDate, eDate, query), status=HTTP_202_ACCEPTED)


class Meetings(APIView):
    def post(self, request):
        return Response(getMeetings(request.data['items'], status=HTTP_202_ACCEPTED))


class RoomMeetings(APIView):
    def post(self, request):
        try:
            a = jwt.decode(request.data['auth_token'], 'secret', algorithm='HS256')
            resource_email = a['email']
            return Response(getMeetingsOfRoomOfaDay(resource_email), status=HTTP_202_ACCEPTED)
        except Exception:
            return Response('Bad Request', status=HTTP_401_UNAUTHORIZED)


class RoomMeetingsTest(APIView):
    def post(self, request):
        try:
            a = jwt.decode(request.data['auth_token'], 'secret', algorithm='HS256')
            resource_email = a['email']
            return Response(getMeetingsOfRoomOfaDaytest(resource_email), status=HTTP_202_ACCEPTED)
        except Exception:
            return Response('Bad Request', status=HTTP_401_UNAUTHORIZED)


class CheckLogin(APIView):
    def post(self, request):
        return Response(checkCredentials(request.data), status=HTTP_202_ACCEPTED)


class RoomDetails(APIView):
    def get(self, request):
        return Response(room_details(), status=HTTP_202_ACCEPTED)


class RegisterResourceForNotification(APIView):
    def get(self, request):
        resources = Resources.objects.all()
        for i in range(resources.count()):
            resources[i].resourceUUID = uuid.uuid4()
            resources[i].save()
            register_resource(resources[i].resourceEmail)
        return Response('ok', status=HTTP_202_ACCEPTED)

    def post(self, request):
        return Response(register_resource(request.data['email']), status=HTTP_202_ACCEPTED)


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class GenearteUserNamePassword(APIView):
    def get(self, request):
        resources = Resources.objects.all()
        for resource in resources:
            resource.roomLoginName = id_generator(6)
            resource.roomPassword = str(id_generator(8, string.digits))
            resource.save()

        return Response('ok', status=HTTP_202_ACCEPTED)


class AddEvent(APIView):
    def post(self, request):
        for event in request.data['items']:
            try:
                if event['status'] == "cancelled":
                    deleteEvent2()
                insertEvent('', event)
            except Exception as e:
                print(e)
        return Response('ok')



@api_view(['GET', 'POST'])
def getchanges(request):
    for obj in Resources.objects.filter(Q(generatedResourceName__icontains='Noida')):
        get_changes(obj.resourceEmail)
    return Response('ok')
