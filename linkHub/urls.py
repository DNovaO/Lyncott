#Urls from linkHub
from django.urls import path
from linkHub.views import *

urlpatterns = [
    path('', linkHub_view, name='linkHub'),
]
