import httplib2
from googleapiclient.discovery import build
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from .models import CredentialsModel
from gfglogin import settings
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from django.shortcuts import render
import apiclient.discovery
from httplib2 import Http
import googleapiclient
import json
import requests




def home(request):
    status = True

    if not request.user.is_authenticated:
        return HttpResponseRedirect('admin')

    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    print(storage)
    credential = storage.get()

    if credential is None or credential.invalid:
        status = False
        print('Not Found')
    else:
        access_token = credential.access_token
        http = httplib2.Http()
        http = credential.authorize(http)
        people_document = "hello world"
        service = build('plus', 'v1', http=http)
        people_resource = service.people()
        people_document = people_resource.get(userId='me').execute()
        print(people_document)
        #print("hellllllo====", data)
    #return HttpResponseRedirect("gmail_authenticate")
    return render(request, 'index.html', {'status': status, 'people_document': people_document})
    #return render(request, 'index.html', {'status': status`})


################################
#   GMAIL API IMPLEMENTATION   #
################################



FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    #scope='https://www.googleapis.com/auth/gmail.readonly',
    scope='https://www.googleapis.com/auth/plus.login https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
    redirect_uri='http://127.0.0.1:8000/oauth2callback',
    prompt='consent')




def gmail_authenticate(request):
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid:
        print("helo========\n")
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                       request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        people_document = "hello world"
        service = build('plus', 'v1', http=http)
        people_resource = service.people()
        people_document = people_resource.get(userId='me').execute()
        #print('ID:' + people_document['id'])
        #print("Display name: " + people_document['displayName'])
        #print("Image URL: " + people_document['image']['url'])
        # #print("Profile URL: " + people_document['url'])
        print(people_document)
        print('access_token = ', credential.access_token)
        status = True
        return render(request, 'index.html', {'status': status, 'people_document': people_document })


#FOR FIRST TIME AUTHENTICATION

def auth_return(request):
    get_state = bytes(request.GET.get('state'), 'utf8')
    if not xsrfutil.validate_token(settings.SECRET_KEY, get_state,
                                   request.user):
        return HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.GET.get('code'))
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    http = httplib2.Http()
    http = credential.authorize(http)
    service = build('plus', 'v1', http=http)
    people_resource = service.people()
    people_document = people_resource.get(userId='me').execute()
    print(people_document)
    status = True
    #print('ID:' + people_document['id'])
    #print("Display name: " + people_document['displayName'])
    #print("Image URL: " + people_document['image']['url'])
    print("access_token: %s" % credential.access_token)
    #return HttpResponseRedirect("/")
    return render(request, 'index.html', {'status': status, 'people_document': people_document})


def logout(request):
    status = False
    DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential').delete()
    #return render(request, 'signup.html')
    return render(request, 'index.html', {'status': status })
