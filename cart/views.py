from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
from cart.models import Cart,CartItem
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from userptofile.models import Address
from offers.models import Coupon
# Create your views here.


def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart


def add_cart(request,product_id):

    current_user=request.user
    product=Product.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))#get the cart id from the above private function(because of the underscore), which is created by session 
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()  

    try:

        cart_item=CartItem.objects.get(product=product,cart=cart,user=current_user)
        cart_item.quantity += 1 #incrementing the cart item
        cart_item.save()

    except CartItem.DoesNotExist:

        cart_item=CartItem.objects.create(

            product = product,
            quantity = 1,
            cart=cart,
            user=current_user

        ) 
    cart_item.save()
    return redirect('cart')
   
    # return HttpResponse(cart_item.product)
    # exit()
def decrement_quantity(request):
    product_id  = request.GET.get('id')
    product = get_object_or_404(Product,id = product_id)
    print(product)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product,user=request.user)
        print(cart_item.product.id)
    else:
        cart_item = CartItem.objects.get(product=product,cart = cart)
        
    
    if cart_item.quantity:
        total_price = 0
        total = 0
        
        qty = cart_item.quantity - 1
        
        cart_item.quantity  = qty
        cart_item.save()

        total_price += (cart_item.product.price * cart_item.quantity)
        total += (cart_item.product.price * cart_item.quantity)
        cart_item.save()
        sub_total =  cart_item.sub_total()

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user = request.user,is_active= True)
        else:
            cart_items = CartItem.objects.filter(cart = cart,is_active =True)

        total_p = 0
        total_price_p = 0

        for cart_item in cart_items:
            total_price_p += (cart_item.product.price * cart_item.quantity)
            total_p += (cart_item.product.price * cart_item.quantity)
            saved_p = total_price_p - total_p
    return JsonResponse({
                'quantity':qty,
                'total': total_p,
                'sub_total':sub_total,
                'total_price': total_price_p,
                'saved':saved_p
        
    })

def increment_cart(request):

    product_id  = request.GET.get('id')
    product = get_object_or_404(Product,id = product_id)
    print("haiiiiiiiiiiii")
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product,user=request.user)
        
    else:
        cart_item = CartItem.objects.get(product=product,cart = cart)
        print(cart_item.id)
    
    if cart_item.quantity:
        total_price = 0
        total = 0

        qty = cart_item.quantity + 1
        
        cart_item.quantity  = qty
        cart_item.save()

        total_price += (cart_item.product.price * cart_item.quantity)
        total += (cart_item.product.price * cart_item.quantity)
        cart_item.save()
        sub_total =  cart_item.sub_total()

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user = request.user,is_active= True)
       
        else:
            cart_items = CartItem.objects.filter(cart = cart,is_active =True)

        total_p = 0
        total_price_p = 0
        for cart_item in cart_items:
            total_price_p += (cart_item.product.price * cart_item.quantity)
            total_p += (cart_item.product.price * cart_item.quantity)
            saved_p = total_price_p - total_p
    return JsonResponse({
                'quantity':qty,
                'total': total_p,
                'sub_total':sub_total,
                'total_price': total_price_p,
                'saved':saved_p
        
    })
def remove_cart(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


    
    

def remove_cart_item(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
       cart_item=CartItem.objects.get(product=product,user=request.user)
    else:
       cart=Cart.objects.get(cart_id=_cart_id(request))
       cart_item=CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')

    
def  cart(request,total=0,quantity=0,cart_items=None):

    try:
       
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            print('>>>>>>>>>>')
            cart_items=CartItem.objects.filter(user=request.user,is_active=True).order_by('id')
            # print(cart_items)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
        
            quantity= cart_item.quantity

        tax=(2 * total)/100
        grand_total=total+tax

    except ObjectDoesNotExist:
        pass

    context={
        'total':total,
        'quantity':quantity,
        'cart_item':cart_items,
        'tax':tax,
        'grand_total':grand_total,

    }
    return render(request,'cart.html',context)

def viewcoupon(request):
    coupon=Coupon.objects.all()
    return render(request,'viewcoupon.html',{'coupon':coupon})

def apply_coupon(request):
   
    pass





@login_required(login_url='user_login')
def checkout(request,total=0,quantity=0,cart_items=None):
    try:
        tax = 0
        grand_total = 0

        # cart=Cart.objects.get(cart_id=_cart_id(request))
        # cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        if request.user.is_authenticated:
            print('>>>>>>>>>>')
            cart_items=CartItem.objects.filter(user=request.user,is_active=True).order_by('id')
            # print(cart_items)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity= cart_item.quantity

        tax=(2 * total)/100
        grand_total=total+tax
        address = Address.objects.filter(user= request.user)
    except ObjectDoesNotExist:
        pass
    context={
        'total':total,
        'quantity':quantity,
        'cart_item':cart_items,
        'tax':tax,
        'address':address,
        'grand_total':grand_total,

    }
    return render(request,'checkout.html',context)


