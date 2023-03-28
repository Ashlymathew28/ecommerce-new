from django.shortcuts import render,redirect
from cart .models import *
from .models import *
from store .models import Product
from .forms import OrderForm
import datetime
from django.http import JsonResponse
# Create your views here.


def payments(request):
     
    return render(request,'payment.html')

def place_order(request):
    total=0
    qunatity=0
    current_user = request.user
    print("keritoo place order ill")
    #if cart count <=0 then redirect to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count  <=  0:
       return redirect('user_shop')

    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        qunatity += cart_item.quantity

    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
            
   
    
        # print("inside post ..............")
        # form = OrderForm(request.POST)
        # if  form.is_valid():
            #store data
            print("entered to function")
            data = Order()
            data.user=request.user
            address_id=request.POST.get('address')
            address = Address.objects.get(id=address_id)
            data.address = address
            print(address_id,'Kitida mwoneeee...')
            print("address evde ind",data.address)
            data.order_note = request.POST.get('order_note')
           
            if data.order_note:
                data.order_note = data.order_note
            else:
                data.order_note = '',

            data.pay_method = request.POST.get('pay_mode')
            data.pay_id = request.POST.get('pay_id')
            print(data.pay_method)
            print(data.pay_id)
            data.order_total = grand_total
            data.tax = tax
            print("order total ethatto :",data.order_total)
            print("tax ethatto: ",data.tax)
            data.save()
            print("save aaayito details okke ")
            #generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date =d.strftime("%Y%m%d")
            order_number = str('1000') + str(data.id)
            data.order_number = order_number
            data.status = "placed"
            data.save()
            print(request.user)
         
            neworderitems = CartItem.objects.filter(user=request.user)
            for item in neworderitems:
                OrderProduct.objects.create(
                    order=data,
                    product = item.product,
                    product_price = item.product.price,
                    quantity=item.quantity,
                    user = request.user,

                )
                orderproduct =Product.objects.filter(id=item.product_id).first()
                print(orderproduct.id,"sadhanam evde ind")
                orderproduct.stock -= item.quantity
                orderproduct.save()
            
            CartItem.objects.filter(user=request.user).delete()
            
            print("jjjjjjjjjj")
            # payMode=request.POST.get('pay_method')
            pay_method = request.POST.get('pay_mode')
            if ( pay_method== "Razorpay"):
                print("payMode")
                return JsonResponse({
                    'status':"Your order has been placed successfully!"
                    })
            return redirect('payments')
        # else:
          
            # return redirect('checkout')
    else:
        print("method is not post")
        return redirect('cart')


def proceed_to_pay(request):
    cartitems = CartItem.objects.filter(user=request.user)
    print('Kuttaaa proceed to payil athitunddd......')
    total_price = 0
    for item in cartitems:
        total_price += (item.product.price * item.quantity)
        price = total_price
        total_price = price
    return JsonResponse({

        'total_price':total_price
    })

def order_cancel(request):
    order_id=request.POST.get('order_id')

    print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK",order_id)
    order=OrderProduct.objects.filter(order_id=order_id).first()
    print(order)
    order.order.status = 'Cancelled'
    print(order.order.status)
    order.order.save()
    order.product.stock += order.quantity
    order.product.save()

    print("order cancelled aayito ")
    return JsonResponse({"status":"Cancelled"})
