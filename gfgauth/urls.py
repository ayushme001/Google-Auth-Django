from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^gmailAuthenticate', views.gmail_authenticate, name='gmail_authenticate'),
    url(r'^oauth2callback', views.auth_return),
    url(r'^$', views.home, name='home'),
    path('logout/', views.logout, name='signup'),
]
