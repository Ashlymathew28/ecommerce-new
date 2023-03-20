from django.shortcuts import render,redirect
from .models import Address
from orders .models import *

# Create your views here.


def userdetails(request):
    return render(request,'userprofile.html')

def useraddress(request):
    # if request.method == 'POST':
    #     print("haiii")
    # else:
    address = Address.objects.filter(user=request.user)
    return render(request,'useraddress.html',{'address':address})


def my_order(request):
    order=OrderProduct.objects.filter(user=request.user)
    context = {'order':order}
    return render(request,'user_orderlist.html',context)

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


class PreUrl:
    url = None
    def __init__(self,destination) -> None:
        PreUrl.url = destination