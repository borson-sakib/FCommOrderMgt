from django.shortcuts import render,redirect

from .models import *
# Create your views here.


def home(request):
    
    return render(request,'POS/home.html')


def sales(request):
    
    pass
def addCategory(request):
    
    if (request.method == 'POST'):
        
        category_name =request.POST['category_name']
        category_id =request.POST['category_id']
        
        print(category_name)
        
        Category.objects.create(
            category_name=category_name,
            category_id= category_id
        )
        
        return redirect('addCategory')
    
    try:
        categories = Category.objects.all()
        print(categories)
    except:
        categories = None
        print(categories)
        
    return render(request,'POS/addCategory.html',{'categories':categories})


def addProducts(request):
    
    if (request.method == "POST"):
        pass

def poswindow(request):
    
    category = Category.objects.all()
    
    context = {'category':category}
    
    return render(request,'POS/poswindow.html',context)