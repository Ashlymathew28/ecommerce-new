from django.shortcuts import render,redirect
from cart .models import *
from .models import *
from store .models import Product
from .forms import OrderForm
import datetime
from django.http import JsonResponse
from django.views.generic import View
from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from django.shortcuts import  render
from xhtml2pdf import pisa




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
        total += (cart_item.product.user_price * cart_item.quantity)
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
            if 'new_price' in  request.session:

                 data.order_total = request.session['new_price']
            else:
                data.order_total =grand_total
            data.tax = tax
            data.save()
            print("cod total",data.order_total)
            print("order total ethatto :",data.order_total)
            print("tax ethatto: ",data.tax)
            
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
            if 'new_price' in request.session:
                request.session.pop('coupon',None)
                request.session.pop('new_price',None)
                request.session.pop('coup_discount',None)
                request.session.modified = True

            pay_method = request.POST.get('pay_mode')
            if ( pay_method== "Razorpay"):
                print("payMode")
                return JsonResponse({
                    'status':"Your order has been placed successfully!",
                    'id':data.id,
                    })
            else:
                return JsonResponse({
                    'id':data.id,
                })
            # return redirect('payments')
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
        total_price += (item.product.user_price * item.quantity)
        price = total_price
        total_price = price
    
    if 'new_price' in request.session:
      total_price=request.session['new_price']
    else:
        tax=(2*total_price)/100
        total_price=total_price+tax
    print("total from proceed to pay",total_price)
    return JsonResponse({

        'total_price':total_price
    })

def order_cancel(request):
    order_id=request.POST.get('order_id')

    print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK",order_id)
    order=OrderProduct.objects.get(id=order_id)
    print(order)
    order.status = 'Cancelled'
    print(order.status)
    order.save()
    order.product.stock += order.quantity
    order.product.save()

    print("ordered Product cancelled aayito ")
    return JsonResponse({"status":"Cancelled"})


def order_return(request):
    order_id=request.POST.get('order_id')
    print("order id: ",order_id)
    order=OrderProduct.objects.get(id=order_id)
    order.status = 'Returned'
    order.save()
    order.product.stock += order.quantity
    order.product.save()
    print("order returned >>>>>>>>>>")
    return JsonResponse({'status':'Returned'})


# generating Invoice
class generateInvoice(View):
    def get(self,request,id,*args,**kwargs):
        try:
            ordersItem=OrderProduct.objects.get(order_id=id,user=request.user)
        except:
            return HttpResponse("505 not found")
        data={
            'order_id':ordersItem.orders.id,
            'date':str(ordersItem.orders.created_at),
            'name':ordersItem.orders.user.first_name,
            'address':ordersItem.orders.address.Address,
            'total_price':ordersItem.orders.order_total,
            'transaction_id':ordersItem.orders.pay_id,
            'payment_mode':ordersItem.orders.pay_method,
            'user_email':ordersItem.orders.user.email,
            'orders':ordersItem.orders
        }
        pdf=render_to_pdf('invoice.html',data)
        return HttpResponse(pdf,content_type='application/pdf')
    
def render_to_pdf(template_src,context_dict={}):
    template=get_template(template_src)
    html=template.render(context_dict)
    result=BytesIO()
    pdf=pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None  
