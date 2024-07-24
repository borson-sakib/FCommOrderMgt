from telnetlib import LOGOUT
from django.contrib import admin
from django.urls import path
from .views import *
# from .utils import *
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.middleware import AuthenticationMiddleware

urlpatterns = [
    
   
    path('home', home, name="home"),
    path('sales', sales, name="sales"),
    path('addCategory', addCategory, name="addCategory"),
    path('poswindow', poswindow, name="poswindow"),
    


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


