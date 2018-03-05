import os
import requests
import logging

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.decorators import api_view

from MyResources.event import insertEvent, deleteEvent2
from MyResources.models import Resources
from django.contrib.sessions.backends.db import SessionStore
from datetime import datetime, timezone

session = SessionStore()

# change this for building docker image
CLIENT_SECRETS_FILE = os.path.join(settings.BASE_DIR, "client_secret.json")

SCOPES = ['https://www.googleapis.com/auth/calendar']
API_SERVICE_NAME = 'calender'
API_VERSION = 'v3'


def callbackauthorized():
    return HttpResponse('authorized')

@api_view(['GET', 'POST'])
def get_events(request):
    for resource in Resources.objects.all():
        try:
            credentials = google.oauth2.credentials.Credentials(**session['credentials'])
            service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
            events = service.events().list(calendarId=resource.resourceEmail).execute()
            for event in events['items']:
                try:
                    if event['status'] == "cancelled":
                        deleteEvent2(resource_email=resource.resourceEmail,eventobject=event)
                    else:
                        insertEvent(resource_email=resource.resourceEmail, eventobject=event)
                except Exception as e:
                    logging.error(e, exc_info=True)
                    print(resource.resourceEmail)
                    print(event['id'])

                resource.syncToken = events['nextSyncToken']
                resource.save()
        except Exception as e:
            print(e)
    return HttpResponse()

def get_changes(resource_email):
    try:
        sync_token = Resources.objects.get(resourceEmail=resource_email).syncToken
        credentials = google.oauth2.credentials.Credentials(**session['credentials'])
        service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
        if sync_token == '':
            events = service.events().list(calendarId=resource_email,
                                           timeMin=datetime.now(timezone.utc).astimezone().isoformat()).execute()
        else:
            events = service.events().list(calendarId=resource_email,
                                           syncToken=sync_token).execute()
        for event in events['items']:
            try:
                if event['status'] == "cancelled":
                    deleteEvent2(resource_email=resource_email,eventobject=event)
                else:
                    insertEvent(resource_email=resource_email, eventobject=event)
            except Exception as e:
                logging.error(e, exc_info=True)
                print(resource_email)
                print(event['id'])

        resource = Resources.objects.get(resourceEmail=resource_email)
        resource.syncToken = events['nextSyncToken']
        resource.save()

        # Save credentials back to session in case access token was refreshed.
        # ACTION ITEM: In a production app, you likely want to save these
        #              credentials in a persistent database instead.
        session['credentials'] = credentials_to_dict(credentials)
    except Exception as e:
        logging.error(e, exc_info=True)


def register_resource(email):
    from django.conf import settings
    try:
        watch_body ={
            "id": Resources.objects.get(resourceEmail=email).resourceUUID,
            "type": "web_hook",
            "address": getattr(settings, 'GOOGLE_PUSH_NOTIFICATION_CALLBACK_URL', None),
            "params": {
                "ttl": '1767225599'
            }

        }
        credentials = google.oauth2.credentials.Credentials(**session['credentials'])
        service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
        a = service.events().watch(calendarId=email, body=watch_body).execute()
        print(a)
    except Exception as e:
        print(e)
    return 'ok'


def authorize(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = '{0}/MyResources/oauth2callback'.format( '{scheme}://{host}'.format(host=request.get_host(),
                                           scheme=request.META.get('HTTP_X_FORWARDED_PROTO', 'http')))

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    session['state'] = state

    return redirect(authorization_url)


def oauth2callback(request):
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)

    flow.redirect_uri = '{0}/MyResources/oauth2callback'.format( '{scheme}://{host}'.format(host=request.get_host(),
                                           scheme=request.META.get('HTTP_X_FORWARDED_PROTO', 'http')))

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.

    authorization_response = str(request)
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return callbackauthorized()


def print_index_table(request):
    return ('<table>' +
            '<tr><td><a href="{0}/MyResources/authorize">Test the auth flow directly</a></td>'.format(
                '{scheme}://{host}'.format(host=request.get_host(),
                                           scheme=request.META.get('HTTP_X_FORWARDED_PROTO', 'http'))
            ) +
            '<td>Go directly to the authorization flow. If there are stored ' +
            '    credentials, you still might not be prompted to reauthorize ' +
            '    the application.</td></tr>' +
            '</table>')


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
