from django.shortcuts import render
from django.template import context
from category.models import category
from adminapp.models import Banner
from store.models import Product
# Create your views here.
def home(request):
    products=Product.objects.all().filter(is_available=True)[:4]
    Category=category.objects.all()
    ban=Banner.objects.all()
    context={
        'products':products,
        'category':Category,
        'ban':ban,
    }
    return render(request,"user_homepage.html",context)

# #product list for users
# def user_shop(request):
#     product=Product.objects.all()
#     Category=category.objects.all()
#     context={
#         'product':product,
#         'category':Category,
#     }
#     return render(request,'listview.html',context)