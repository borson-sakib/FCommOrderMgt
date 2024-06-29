from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from urllib import request
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
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
    products=Product.objects.filter(shop=shop)
    
    print(products)
    
    return render(request,'shopView.html',{'shop':shop,'products':products})

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
        
        print({os.path.splitext(product_image.name)[1]})
        # Get next serial number for the shop and category
        serial_number = Product.get_next_serial_number(shop_instance_id, product_category)

        # Generate the new image name
        new_image_name = f"{shop_instance_id}-{product_category}-proSL-{serial_number:04d}{os.path.splitext(product_image.name)[1]}"
        print('-------------')
        print(new_image_name)
        
        image_dir = os.path.join(settings.MEDIA_ROOT, 'products')
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        
        image_path = os.path.join(image_dir, new_image_name)
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
        category=product_category,
        description = product_description,
        price = product_price,
        stock = 1099,
        image = 'products/' + new_image_name,
        )
    
    return render(request,'addProducts.html',{'shop':shop_instance})



def userProfile(request,shop_id_public):
    
    shop_instance=get_object_or_404(Shop, shop_id_public=shop_id_public)

    
    return render(request,'user/userProfile.html',{'shop':shop_instance})

def testURL(request):
    
    
    latest_product = Product.objects.filter(shopid='waffle-theory', category='Food').order_by('-serial_no').first()
    print(latest_product)
    if latest_product and latest_product.image:
        serial_number = int(latest_product.image.name.split('-')[-1].split('.')[0])
        print(serial_number)
        return serial_number + 1
    return HttpResponse('Noe')

def updateShopLogo(request,shop_id_public):
    shop_instance=get_object_or_404(Shop, shop_id_public=shop_id_public)
    shop_instance_id=shop_instance.shop_id_public
    if request.method == 'POST':
        shop_logo=request.FILES['shop_logo']
        
        new_image_name = f"{shop_instance_id}-logo{os.path.splitext(shop_logo.name)[1]}"
        print('-------------')
        print(new_image_name)
        
        image_dir = os.path.join(settings.MEDIA_ROOT, 'shop_resources/logo')
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        
        image_path = os.path.join(image_dir, new_image_name)
        with open(image_path, 'wb+') as destination:
            for chunk in shop_logo.chunks():
                destination.write(chunk)
                
        shop_instance.shop_logo='shop_resources/logo/' + new_image_name
        shop_instance.save()
        
        # Get the current URL with parameters
        baseurl = "http://127.0.0.1:8000/userProfile"
        
        current_url = f"{baseurl}/{shop_instance_id}"
        
        return HttpResponseRedirect(current_url)
        
        # return redirect('userProfile')
    
    