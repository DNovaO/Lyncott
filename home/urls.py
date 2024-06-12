#Urls from home
from django.urls import path
from .views import home_view
from informes.views import report_view

urlpatterns = [
    path('', home_view, name='home'),
    path('report/', report_view, name='report'), 
]
