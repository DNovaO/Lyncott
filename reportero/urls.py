from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
]

urlpatterns += staticfiles_urlpatterns()

