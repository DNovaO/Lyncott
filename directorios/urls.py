#urls de directorios
from django.urls import path
from .views import directorios_view

urlpatterns = [
    path('', directorios_view, name='directorios'),
]
