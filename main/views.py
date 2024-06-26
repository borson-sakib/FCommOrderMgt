from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from urllib import request
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import *
# Create your views here.


def dashboard(request):
    
    return render(request,'dashboard.html')

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
        
        return HttpResponse(email + mobile + shopname) 

    return HttpResponse('okay!')
    
def userEnd(request):
    
    return render(request,'user/userRegistration.html')
    