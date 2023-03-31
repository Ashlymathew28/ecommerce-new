from django.shortcuts import render,redirect
from .models import Address
from django.http import JsonResponse
from orders .models import *
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

# Create your views here.


def userdetails(request):
    # user=Account.objects.filter(user=request.user)
    return render(request,'userprofile.html')

def useraddress(request):
    # if request.method == 'POST':
    #     print("haiii")
    # else:
    address = Address.objects.filter(user=request.user)
    return render(request,'useraddress.html',{'address':address})


def my_order(request):
    order=Order.objects.filter(user=request.user)
    paginator=Paginator(order,10)
    page=request.GET.get('page')
    paged_order=paginator.get_page(page)
    context = {'order':paged_order}
    return render(request,'user_orderlist.html',context)

def orderDetails(request,id):
    print("orderDetails")
    print(id)
    
    # order=Order.objects.filter(id=id)
    orderItem=OrderProduct.objects.filter(order=id)
    print(orderItem,'/////////')
    # print("////////////Address: ",orderItem.order.address.Address)
    return render(request,'orderDetails.html',{'orderItem':orderItem})



def userAddAddress(request):
    dest = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        print("haiiiiii")
        data = Address()
        # pincode = request.POST.get('pincode')
        # print(pincode)
        data.user=request.user
        data.fname = request.POST.get('first_name')
        data.lname = request.POST.get('last_name')
        # data.phone = request.POST.get('phone')
        data.email = request.POST.get('email')
        data.Address = request.POST.get('address_line_1')
            # data.address_line_2 = request.POST.get('address_line_2')
        data.country = request.POST.get('country')
        data.state = request.POST.get('state')
        data.city = request.POST.get('city')
        data.pincode = request.POST.get('pincode')
        data.save()
        print("saved")
        next = PreUrl.url
        return redirect(next)
        # return render(request,'addressForm.html')
    else:
         instance = Address()
    PreUrl(dest)
    return render(request,'addressForm.html')

def edit_address(request,id):
    if request.method == 'POST':
        print("haiiiiii")
        data = Address.objects.get(id=id)
        # pincode = request.POST.get('pincode')
        # print(pincode)
        data.user=request.user
        data.fname = request.POST.get('first_name')
        data.lname = request.POST.get('last_name')
        # data.phone = request.POST.get('phone')
        data.email = request.POST.get('email')
        data.Address = request.POST.get('address_line_1')
            # data.address_line_2 = request.POST.get('address_line_2')
        data.country = request.POST.get('country')
        data.state = request.POST.get('state')
        data.city = request.POST.get('city')
        data.pincode = request.POST.get('pincode')
        data.save()
        print("saved")
        return redirect('useraddress')
        # return render(request,'addressForm.html')
    
    
    else:
        data=Address.objects.get(id=id)
        print("address: ",data)
        return render(request,'edit_address.html',{'data':data})
    
def deleteAddress(request):
    id=request.GET.get('id')
    remove=Address.objects.get(id=id).delete()
    return JsonResponse({'status':'true'})

class PreUrl:
    url = None
    def __init__(self,destination) -> None:
        PreUrl.url = destination