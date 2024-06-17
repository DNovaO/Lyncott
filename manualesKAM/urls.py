#urls de manuales
from django.urls import path
from .views import manuales_view

urlpatterns = [
    path('', manuales_view, name='manuales'),
]
