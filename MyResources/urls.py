from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from MyResources import views, fetchCalenderData


urlpatterns = [
    path('addresources',views.AddMutlipleResources.as_view()),
    path('addresource', views.AddResource.as_view()),
    path('watch', views.notify),
    path('test1',views.test),
    path('oauth2callback', fetchCalenderData.oauth2callback),
    path('authorize', fetchCalenderData.authorize),
    path('overallstats',views.OverallStats.as_view()),
    path('roomstats',views.RoomStats.as_view()),
    path('getMeetings',views.Meetings.as_view()),
    path('gettodaysMeetingsofroom', views.RoomMeetings.as_view()),
    path('gettodaysMeetingsofroomtest', views.RoomMeetingsTest.as_view()),
    path('login', views.CheckLogin.as_view()),
    path('register', views.RegisterResourceForNotification.as_view()),
    path('setcredentials',views.GenearteUserNamePassword.as_view()),
    path('insert', views.AddEvent.as_view()),
    path('getAllEvents',views.get_events),
    path('getEventsAfter',views.get_events_after),
    path('roomDetails',views.RoomDetails.as_view()),
    path('dashboardLogin',views.dashboard_login)

]

urlpatterns = format_suffix_patterns(urlpatterns)