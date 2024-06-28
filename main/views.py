from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from urllib import request
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import requests
import os
from .models import *
# Create your views here.


def dashboard(request):
    
    current_location = get_location()
    shop_count=Shop.objects.count()
    
    print(current_location) 
    
    return render(request,'home.html',{'location':current_location,'shop_count':shop_count})

def shops(request):
    
    shops = Shop.objects.all()
    
    return render(request, 'shops.html', {'shops': shops})

def shopView(request,shop_id_public):
    
    shop = get_object_or_404(Shop, shop_id_public=shop_id_public)
    
    print(shop)
    
    return render(request,'shopView.html',{'shop':shop})

def shopViewTest(request):
    
    
    return render(request,'shopView.html')

def createShop(request):
    
    if request.method == 'POST':
        
        email=request.POST['email']
        mobile=request.POST['mobile']
        shopname=request.POST['shopname']
        
        OwnerDetails.objects.create(
            email=email,
            mobile=mobile,
            primaryshopname=shopname
        )
        
        
        try:
            Shop.objects.create(
            shop_name = shopname,
            location = get_location(),
            owner_name = 'test',
            contact_phone=mobile,
            contact_email = email,
            )
            print('Successfully created A shop')
        except:
            print('Failed to save shop')
        return redirect('shops') 

    return HttpResponse('okay!')
    
def userEnd(request):
    
    return render(request,'user/userRegistration.html')
    
    
from geopy.geocoders import Nominatim

def get_location():
    # Use ipinfo.io to get the IP address location
    response = requests.get('https://ipinfo.io/')
    data = response.json()
    loc = data['loc'].split(',')
    latitude = loc[0]
    longitude = loc[1]

    print(data['region'])
    # Use geopy to get the address
    # geolocator = Nominatim(user_agent="geoapiExercises")
    # location = geolocator.reverse(f"{latitude}, {longitude}")

    return data['region']


# utils.py or wherever appropriate
from .models import OwnerDetails, Shop
from django.db import IntegrityError

def load_shop_details(request):
    owners = OwnerDetails.objects.all()
    for owner in owners:
        shop_name = owner.primaryshopname
        if not Shop.objects.filter(shop_name=shop_name).exists():
            try:
                Shop.objects.create(
                    shop_name = shop_name,
                    location = get_location(),
                    owner_name = 'test',
                    contact_email = owner.email,
                    contact_phone=owner.mobile,
                    )
                print(f"Shop '{shop_name}' added.")
            except IntegrityError:
                print(f"Shop '{shop_name}' already exists (handled by IntegrityError).")
        else:
            print(f"Shop '{shop_name}' already exists (handled by exists() check).")

    return redirect('shops')
# You can call this function to perform the operation


def addProduct(request,shop_id_public):
    
    shop_instance=get_object_or_404(Shop, shop_id_public=shop_id_public)
    shop_instance_id=shop_instance.shop_id_public
    
    if request.method == 'POST':
        
        product_name= request.POST['product_name']
        product_category= request.POST['product_category']
        product_price= request.POST['product_price']
        product_description= request.POST['product_description']
        product_image= request.FILES['product_image']
        
        image_dir = os.path.join(settings.MEDIA_ROOT, 'products')
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        
        image_path = os.path.join(image_dir, product_image.name)
        with open(image_path, 'wb+') as destination:
            for chunk in product_image.chunks():
                destination.write(chunk)
        
        print(product_name)
        print(product_category)
        print(product_price)
        print(product_description)
        print(product_image)
        
        
        Product.objects.create(
        shop = shop_instance,
        shopid = shop_instance_id,
        name = product_name,
        description = product_description,
        price = product_price,
        stock = 1099,
        image = 'products/' + product_image.name,
        )
    
    return render(request,'addProducts.html',{'shop':shop_instance})