from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
from cart.models import Cart,CartItem,Wishlist
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from userptofile.models import Address
from django.core.paginator import Paginator

from offers.models import Coupon
import datetime
# Create your views here.


def _cart_id(request):
    cart=request.session.session_key
    
    if not cart:
        cart=request.session.create()
    return cart

def _wish_id(request):
    wish=request.session.session_key
    
    if not wish:
        wish=request.session.create()
    return wish

@login_required(login_url='user_login')
def add_cart(request,product_id):

    current_user=request.user
    product=Product.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))#get the cart id from the above private function(because of the underscore), which is created by session 
        print("userrrrrr:",cart)
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_cart_id(request)
        )
        print("carttttt : ",cart)
    cart.save()  

    if current_user.is_authenticated:
        try:

            cart_item=CartItem.objects.get(product=product,cart=cart,user=current_user)
            print("uiuiuiuiuiuiuiuuiuiuiuiiui",cart_item)
            cart_item.quantity += 1 #incrementing the cart item
            cart_item.save()

        except CartItem.DoesNotExist:

            cart_item=CartItem.objects.create(

                product = product,
                quantity = 1,
                cart=cart,
                user=current_user

            ) 
    else:
        print("elseeeeeeeee")
        if CartItem.objects.filter(product=product,cart=cart).exists():
            print("product: ",product)
            cart_item=CartItem.objects.get(product=product,cart=cart)
            print("cart_item : ",cart_item)
            cart_item.quantity += 1 #incrementing the cart item
            cart_item.save()

        else:

            cart_item=CartItem.objects.create(

                product = product,
                quantity = 1,
                cart=cart,
               

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
        try:
            cart=Cart.objects.get(cart_id = _cart_id(request))
            cart.save()
        except Cart.DoesNotExist:
            cart=Cart.objects.create(cart_id = _cart_id(request))
            cart.save()

        cart_item = CartItem.objects.get(product=product,cart = cart)
        
    if product.stock > 0:
        if cart_item.quantity :
            total_price = 0
            total = 0
            
            qty = cart_item.quantity - 1
            
            cart_item.quantity  = qty
            cart_item.product.stock += 1
            cart_item.product.save()
            
            cart_item.save()

            total_price += (cart_item.product.user_price * cart_item.quantity)
            total += (cart_item.product.user_price * cart_item.quantity)
            cart_item.save()
            sub_total =  cart_item.sub_total()

            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user = request.user,is_active= True)
            else:
                cart_items = CartItem.objects.filter(cart = cart,is_active =True)

            total_p = 0
            total_price_p = 0

            for cart_item in cart_items:
                total_price_p += (cart_item.product.user_price * cart_item.quantity)
                total_p += (cart_item.product.user_price * cart_item.quantity)
                saved_p = total_price_p - total_p
        # else:
        #     cart_item.delete()
            print("decreement")
            print("total_price_p",total_price_p)
            print("total_price",total_price)
            print("sub_price",sub_total)

            tax=(2 * total_price_p)/100
            print(tax)
            grand_total=tax+total_price_p
            print(grand_total)
        print
        return JsonResponse({
                    'quantity':qty,
                    'total': total_price,
                    'grand_total': grand_total,
                    'tax': tax,
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
        try:
            cart=Cart.objects.get(cart_id = _cart_id(request))
            cart.save()
        except Cart.DoesNotExist:
            cart=Cart.objects.create(cart_id = _cart_id(request))
            cart.save()

        cart_item = CartItem.objects.get(product=product,cart = cart)
        print("cat:",cart)
        print(cart_item.id)
    
    if product.stock > 0:
        
        total_price = 0
        total = 0

        qty = cart_item.quantity + 1
        
        cart_item.quantity  = qty
        cart_item.product.stock -= 1
        cart_item.product.save()
        cart_item.save()

        total_price += (cart_item.product.user_price * cart_item.quantity)
        total += (cart_item.product.user_price * cart_item.quantity)
        cart_item.save()
        sub_total =  cart_item.sub_total()

        if request.user.is_authenticated:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>")
            cart_items = CartItem.objects.filter(user = request.user,is_active= True)
       
        else:
            print("?////////////////////////////////")
            # cart=Cart.objects.get()
            cart_items = CartItem.objects.filter(cart = cart,is_active =True)

            print(cart_item)

        total_p = 0
        total_price_p = 0
        for cart_item in cart_items:
            total_price_p += (cart_item.product.user_price * cart_item.quantity)
            total_p += (cart_item.product.user_price * cart_item.quantity)
            saved_p = total_price_p - total_p

        print("total_p",total_p)
        print("sub_total",sub_total)
        print("total_price",total_price)
        tax=(2 * total_p)/100
        print(tax)
        grand_total=tax+total_p
        print(grand_total)
    return JsonResponse({
                'grand_total':grand_total,
                'quantity':qty,
                'total': total_p,
                'sub_total':sub_total,
                'total_price': total_price_p,
                'tax':tax,
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


    
    

def remove_cart_item(request):
    product_id=request.GET.get('id')
    product=get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
       cart_item=CartItem.objects.get(product=product,user=request.user)
    else:
       cart=Cart.objects.get(cart_id=_cart_id(request))
       cart_item=CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    print("removeeeeeeeeeeeee")
    # return redirect('cart')
    return JsonResponse({'status':'true'})

    
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

                total += (cart_item.product.user_price * cart_item.quantity)
        
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

def Whislist(request):
    if request.user.is_authenticated:
       print("tryyyyy")
       wish=Wishlist.objects.filter(user=request.user)
    else:
        print("cacheeee")
        wish=Wishlist.objects.filter(wish_id=_wish_id(request))
    print(wish)
    return render(request,'wishlist.html',{'wish':wish})

def AddWhishlist(request):

    # if request.method == 'POST':
        print("add wishlist")
        if request.user.is_authenticated:
            prod_id = request.GET.get('product_id')
            print(prod_id)
            product_check = Product.objects.get(id=prod_id)

            if(product_check):
                print("prod_check : ",product_check)
                if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                    return JsonResponse({'status':"Product already in wishlist"})

                else:
                    Wishlist.objects.create(user=request.user, product_id=prod_id)
                    return JsonResponse({'status':"Product added to wishlist"})

            else:
                return JsonResponse({'status':"No such product found"})

        else:
            return JsonResponse({'status':"Login to continue"})

    # return redirect("/")

def removeWish(request,id):
    product=get_object_or_404(Product,id=id)
    if request.user.is_authenticated:
       wishlist=Wishlist.objects.get(product=product,user=request.user)
    else:
       wishlist=Wishlist.objects.get(product=product,wish_id=_wish_id(request))
    #    cart_item=CartItem.objects.get(product=product,cart=cart)
    wishlist.delete()
    print("removeeeeeeeeeeeee")
    return redirect(request.META.get('HTTP_REFERER'))

def viewcoupon(request):
    coupon=Coupon.objects.all()
    return render(request,'viewcoupon.html',{'coupon':coupon})

def apply_coupon(request):
    print("coupon : ")
    d   = datetime.datetime.today()
    now = datetime.date(d.year,d.month,d.day)
    print(now)
    code=request.GET.get('coupon_code')
    total=float(request.GET.get('grand_total'))
    tax=float(request.GET.get('tax'))
    print("code>>>>>>>>>>  :",code)
    print('total ; ',total)
    print('tax ; ',tax)
    coup_discount=0

    coupon=Coupon.objects.all()
    verify="nil"
    for i in coupon:
        print(i)
        print(".............>>>>>>>>>>>>>>>>>>>>.............")
        if code ==  i.coupon_code:
            print(" if ill keri.........")
            verify=i.coupon_code
            print("verifyyyy",verify)
    
    if verify == "nil":
        return redirect('checkout')
    
    coup=Coupon.objects.get(coupon_code=verify)
    print("c :::::::",coup)
    print("valid from :",coup.valid_from)
    print("valid to : ",coup.valid_to)
    if now >= coup.valid_from and now <= coup.valid_to:
        coup.active=True
        print("date /////// ") 
        
        coup_price= float(total) - coup.limited_price
        print("coupon price",coup_price)
        discount=total - (total*coup.discount)/100
        print(discount)
        if coup_price  < discount :
            
            new_price = coup_price+tax
            print("new_price : ",new_price)
            coup_discount = coup.limited_price
        else:
            new_price = discount + tax
            print("coupon koiiiiii : ",new_price)
            coup_discount=(total*coup.discount)/100
        coup.save()

        request.session['new_price']=new_price
        request.session['coupon'] = verify
        request.session['coup_discount'] = coup_discount
        print("lasttt")
        return JsonResponse({
            'grand_total':new_price,
            'Coupon':coup_discount,
            'Coupon_code':verify,
        }) 
    
    else:
        coup.active=False
        coup.save()
        print(' ]]]]]]]]]]]]]]]]]]]]]]]]]]]]  ')
        return JsonResponse({
            'Coupon':coup_discount,
            'Coupon_code':'Coupon is not valid !!',


        })
    
def delete_coupon(request):
    code=request.session['coupon']
    print("coupon code",code)
    request.session.pop('coupon',None)
    request.session.pop('new_price',None)
    request.session.pop('coup_discount',None)
    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER'))




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
            total += (cart_item.product.user_price * cart_item.quantity)
            quantity= cart_item.quantity

        tax=(2 * total)/100
        grand_total=total+tax
        address = Address.objects.filter(user= request.user)
        coupon=0
        if 'new_price' in request.session:
            new_price=request.session['new_price']
            coupon=request.session['coupon']
            coupon_dis=request.session['coup_discount']
            if new_price is not None:
                grand_total=new_price
        else:
            coupon="Nil"
            coupon_dis=0
    except ObjectDoesNotExist:
        pass
    context={
        'total':total,
        'quantity':quantity,
        'cart_item':cart_items,
        'tax':tax,
        'Coupon_code':coupon,
        'Coupon':coupon_dis,
        'address':address,
        'grand_total':grand_total,

    }
    return render(request,'checkout.html',context)


