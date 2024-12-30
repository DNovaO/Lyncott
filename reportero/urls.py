#urls.py Main
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from users.views import *
from home.views import *
from informes.views import *
from manualesKAM.views import *
from directorios.views import *
from linkHub.views import *
from dashboard.views import *

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para la administración de Django
    path('', include('users.urls')),  # URL base que incluye las URLs de la aplicación users
    path('home/', include('home.urls')),  # URLs relacionadas con la aplicación home
    path('report/', include('informes.urls')),  # URLs relacionadas con la aplicación informes
    path('KAM/', include('manualesKAM.urls')),  # URLs relacionadas con la aplicación manualesKAM
    path('directorio/', include('directorios.urls')),  # URLs relacionadas con la aplicación directorios
    path('linkHub/', include('linkHub.urls')),  # URLs relacionadas con la aplicación linkHub
    path('dashboard/', include('dashboard.urls')),  # URL para el dashboard
]

urlpatterns += staticfiles_urlpatterns()  # Incluir las URLs estáticas para el manejo de archivos estáticos

