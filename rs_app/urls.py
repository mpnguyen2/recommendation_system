from django.contrib import admin
from django.urls import path, include
#from django.conf.urls import url
from rs_app.views import *

urlpatterns = [
    path('rate/', rate_form),
    path('search/', search_result)
]
'''
patterns('',
    ('^hello/$', hello),
    ('^time/$', current_datetime),
)
'''
#ReactView.as_view()