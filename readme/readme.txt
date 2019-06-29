if you find this error
/google-login/myvenv/lib/python3.5/site-packages/oauth2client/contrib/django_util/__init__.py Line 233

open this file location.
first replace that import from django.core import urlresolvers to from django.urls import reverse
And then replace Line 411 urlresolvers.reverse(...) to reverse(...)
and also in views.py in same folder
