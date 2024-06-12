from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from users.views import *
from home.views import *
from informes.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),  
    path('home/',include('home.urls')),
    path('report/',include('informes.urls')),
]

urlpatterns += staticfiles_urlpatterns()

