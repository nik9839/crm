from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('addEvent', views.AddEvent.as_view()),
    path('addResource',views.AddResource.as_view()),
    path('users', views.UserList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)