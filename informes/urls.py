# informes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_view, name='report'),
]
