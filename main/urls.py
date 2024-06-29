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
    
    #User
    path('userProfile/<str:shop_id_public>', userProfile, name="userProfile"),
    path('updateShopLogo/<str:shop_id_public>', updateShopLogo, name="updateShopLogo"),

   
    path('', dashboard, name="dashboard"),
    path('createShop', createShop, name="createShop"),
    path('userEnd', userEnd, name="userEnd"),
    path('shops', shops, name="shops"),
    path('shopViewTest', shopViewTest, name="shopViewTest"),
    path('shopView/<str:shop_id_public>', shopView, name="shopView"),
    path('load_shop_details', load_shop_details, name="load_shop_details"),
    
   #Products
    path('addProduct/<str:shop_id_public>', addProduct, name="addProduct"),

    #test
    path('testURL', testURL, name="testURL"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


