from django.shortcuts import render,redirect
from .models import Account
from .otp import MessageHandler
from cart.views import _cart_id
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from twilio.rest import Client
from cart.models import *
import requests

import random
# Create your views here.

def homepage(request):
    #if request.user.is_authenticated:
    return render(request,'user_homepage.html')

@never_cache
def user_login(request):
    if request.user.is_superuser:
        return redirect('admin_login')
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        email=request.POST['email']
        # username=request.POST['username']
        
        password=request.POST['password']
        print(email)
        #print("GG",username )
        
        user=authenticate(request,email=email,password=password)
        
        
        print(user)
        print("111")
        if user is not None and user.blocked == False:
            if user.is_superuser == False:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter( cart=cart).exists()
                    if is_cart_item_exists:
                        cart_item = CartItem.objects.filter(cart=cart)
                        for item in cart_item:
                            item.user = user
                            if CartItem.objects.filter(product=item.product,user=user).exists():
                                item_c = CartItem.objects.get(product = item.product,user =user)
                                item_c.quantity += item.quantity
                                item.save()
                            else:
                                item.save()
                except:
                        print('entered in expect ')
                        pass

                login(request,user)
                print("111")
                
                url = request.META.get('HTTP_REFERER')
                try:
                    print("trryyyyyy")
                    print("url = ",url)
                    query=requests.utils.urlparse(url).query
                    print('query= ',query)
                    params=dict(x.split('=')for x in query.split('&'))
                    if 'next' in params:
                        nextPage=params['next']
                        return redirect(nextPage)
                    
                except:
                    print("except")
                    return redirect('homepage')
            else:
                return redirect('admin_login')
        else:
            messages.error(request,'Invalid credentilas')
            return redirect('user_login')
    else:
        return render(request,'member-login.html')

def user_register(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method =='POST':
        user_email=request.POST['email']
        user_name=request.POST.get('username')
        phone_number=request.POST['phone_number']
        password=request.POST['password']
        #confirm_password=request.POST['confirm_password']
        #if password==confirm_password:
        print("ottppp register")
        if Account.objects.filter(email=user_email).exists():
            messages.error(request,'This is email has already an account!!')
            return redirect('user_register')
             #return render(request,'member-register.html',{'error_msg':"This email have already an account!!"})

        else:
            # otp = 1
            # message_handler=MessageHandler(phone_number,otp).send_otp()

            user=Account.objects.create_user(username=user_name,email=user_email,password=password,phone_number=phone_number)
            user.save()
            print(password)
            login(request,user)
            print('user reated')
            return redirect('homepage')

            # context={

            #     'phone_number':phone_number,
            #     'user_email':user_email,
            #     'user_name':user_name,
            #     'password': password


            # }
            # return render(request,'otp.html',context)
        #else:
            #return render(request,'member-register.html',{'error_msg':"Wrong passord"})
    else:
        return render(request,'member-register.html')

def otp_validate(request):
    if request.method == 'POST' and request.POST['otpnumber']:
        print('ttttttttttttttttttttttttttt')
        otp1 = request.POST['otpnumber']
        print(otp1)
        phone_number = request.POST['phone_number']
        user_name=request.POST['user_name']
        user_email=request.POST.get('user_email')
        password=request.POST.get('password')
        validate=MessageHandler(phone_number,otp1).validate()
        print(validate,'jjjjjjjjjjjjjjjjjjjjj')

        if validate == 'approved':
            print('oooooooooooooooooo')
            user=Account.objects.create_user(username=user_name,email=user_email,password=password,phone_number=phone_number)
            user.save() 
            
            print('user reated')
            return redirect('homepage')
        else:
            messages.info(request,'Wrong OTP')
            context={

                'phone_number':phone_number,
                'user_email':user_email,
                'user_name':user_name,
                'password': password

            }
            return render(request,'otp.html',context)
    return render(request,'otp.html')
        
@never_cache
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('homepage')
    else:
        print("user is not authenticated !!!")
        return redirect('homepage')
    