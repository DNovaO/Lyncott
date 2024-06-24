#Urls from home
from django.urls import path
from .views import home_view
from informes.views import *

urlpatterns = [
    path('', home_view, name='home'),
]
