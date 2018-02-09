import os
import requests

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from MyResources.insert import insertEvent


from django.contrib.sessions.backends.db import SessionStore

session = SessionStore()

CLIENT_SECRETS_FILE = "/home/nikhil/Downloads/client_secret.json"


SCOPES = ['https://www.googleapis.com/auth/calendar']
API_SERVICE_NAME = 'calender'
API_VERSION = 'v3'

def callbackauthorized():
    return HttpResponse('authorized')

def test_api_request(resource_email):
    if 'credentials' not in session:
        return authorize('ok')

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])

    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
    events = service.events().list(calendarId=resource_email,
                                   orderBy='updated').execute()
    print(len(events['items']))
    print(events['items'][-1]['summary'])
    data = (events['items'][-1])
    insertEvent(resource_email=resource_email,eventobject=data)
    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    session['credentials'] = credentials_to_dict(credentials)

    return 'ok'


def authorize(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = 'https://crmtest.pagekite.me/MyResources/oauth2callback'

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

    flow.redirect_uri = 'https://crmtest.pagekite.me/MyResources/oauth2callback'

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.

    authorization_response = str(request)
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return callbackauthorized()


def revoke():
  if 'credentials' not in session:
    return ('You need to <a href="/authorize">authorize</a> before ' +
            'testing the code to revoke credentials.')

  credentials = google.oauth2.credentials.Credentials(
    **session['credentials'])

  revoke = requests.post('https://accounts.google.com/o/oauth2/revoke',
      params={'token': credentials.token},
      headers = {'content-type': 'application/x-www-form-urlencoded'})

  status_code = getattr(revoke, 'status_code')
  if status_code == 200:
    return('Credentials successfully revoked.' + print_index_table())
  else:
    return('An error occurred.' + print_index_table())



def clear_credentials():
  if 'credentials' in session:
    del session['credentials']
  return ('Credentials have been cleared.<br><br>' +
          print_index_table())

def print_index_table():
  return ('<table>' +
          '<tr><td><a href="http://127.0.0.1:8000/MyResources/test">Test an API request</a></td>' +
          '<td>Submit an API request and see a formatted JSON response. ' +
          '    Go through the authorization flow if there are no stored ' +
          '    credentials for the user.</td></tr>' +
          '<tr><td><a href="http://127.0.0.1:8000/MyResources/authorize">Test the auth flow directly</a></td>' +
          '<td>Go directly to the authorization flow. If there are stored ' +
          '    credentials, you still might not be prompted to reauthorize ' +
          '    the application.</td></tr>' +
          '<tr><td><a href="http://127.0.0.1:8000/MyResources/revoke">Revoke current credentials</a></td>' +
          '<td>Revoke the access token associated with the current user ' +
          '    session. After revoking credentials, if you go to the test ' +
          '    page, you should see an <code>invalid_grant</code> error.' +
          '</td></tr>' +
          '<tr><td><a href="http//127.0.0.1:8000/MyResources/clear">Clear Flask session credentials</a></td>' +
          '<td>Clear the access token currently stored in the user session. ' +
          '    After clearing the token, if you <a href="/test">test the ' +
          '    API request</a> again, you should go back to the auth flow.' +
          '</td></tr></table>')

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}