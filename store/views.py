from django.shortcuts import render,get_object_or_404
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from cart.views import _cart_id
from .models import Product
from django.http import HttpResponse,HttpResponseRedirect
from cart.models import CartItem,Cart
from category.models import category
# Create your views here.


def search(request):
    Category=category.objects.all()
    if 's' in request.GET:
        keyword=request.GET['s']
        if keyword:
            products=Product.objects.order_by('id').filter(product_name__icontains=keyword)
        else:
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
    paginator=Paginator(products,4)
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)   
    context={
        'products':paged_products,
        'Category':Category
    }
    return render(request,'gridview.html',context)
 


# #product list for users
def user_shop(request,category_slug=None):
    categories=None
    products=None
    if category_slug !=None:
        categories=get_object_or_404(category,cat_slug=category_slug)
        products=Product.objects.all().filter(category=categories,is_available=True)
        # product_count=products.count()
        paginator=Paginator(products,4)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
    else:
        products=Product.objects.all().filter(is_available=True).order_by('id')
        paginator=Paginator(products,4)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        # product_count=product_count() for counting the total product
    # product=Product.objects.all()
    Category=category.objects.all()
    context={
        'products':paged_products,
        'Category':Category,
        # 'product_count':product_count

    }
    return render(request,'gridview.html',context)

def product_detail(request,category_slug,product_slug):

    Category=category.objects.all()
    single_product=Product.objects.get(category__cat_slug=category_slug,prod_slug=product_slug)
    # if request.user.is_authenticated:
    #     cart=Cart.objects.filter(user=request.user).first()
    #     if cart:
    #         in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    # else:
    if request.user.is_authenticated:
        in_cart=CartItem.objects.filter(user=request.user,product=single_product).exists()
    else:
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()

    context={
        'single_product':single_product,
        'Category':Category,
        'in_cart':in_cart
    }

    return render(request,'product_detail.html',context)