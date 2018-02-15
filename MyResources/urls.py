from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from MyResources import views, fetchCalenderData


urlpatterns = [

    path('addresource', views.AddResource.as_view()),
    path('watch', views.notify),
    path('test1',views.test),
    path('oauth2callback', fetchCalenderData.oauth2callback),
    #path('test', fetchCalenderData.test_api_request),
    path('authorize', fetchCalenderData.authorize),
    #path('revoke', fetchCalenderData.revoke),
    #path('clear', fetchCalenderData.clear_credentials),
    path('overallstats',views.OverallStats.as_view()),
    path('roomstats',views.RoomStats.as_view()),
    path('getMeetings',views.Meetings.as_view()),
    path('getMeetings2', views.getMeetings2)

]

urlpatterns = format_suffix_patterns(urlpatterns)