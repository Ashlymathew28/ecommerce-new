from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import category
# Create your views here.


# #product list for users
def user_shop(request,category_slug=None):
    categories=None
    products=None
    if category_slug !=None:
        categories=get_object_or_404(category,cat_slug=category_slug)
        products=Product.objects.all().filter(category=categories,is_available=True)
        # product_count=products.count()
    else:
        products=Product.objects.all().filter(is_available=True)
        # product_count=product_count()
    # product=Product.objects.all()
    Category=category.objects.all()
    context={
        'products':products,
        'Category':Category,
        # 'product_count':product_count

    }
    return render(request,'listview.html',context)

def product_detail(request,category_slug,product_slug):
    Category=category.objects.all()
    single_product=Product.objects.get(category__cat_slug=category_slug,prod_slug=product_slug)
    context={
        'single_product':single_product,
        'Category':Category
    }

    return render(request,'product_detail.html',context)