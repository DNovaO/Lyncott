from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login_redirect'),  
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),
]

urlpatterns += staticfiles_urlpatterns()

