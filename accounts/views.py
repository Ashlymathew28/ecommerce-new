from django.shortcuts import render,redirect
from .models import Account
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.

def homepage(request):
    #if request.user.is_authenticated:
    return render(request,'user_homepage.html')

def user_login(request):
 
    if request.method == 'POST':
        email=request.POST['email']
        #username=request.POST['username']
        
        password=request.POST['password']
        print(email)
        #print("GG",username )
        
        user=authenticate(request,email=email,password=password)
        
        
        print(user)
        print("111")
        if user is not None:
            login(request,user)
            print("111")
            return redirect('homepage')
        else:
            messages.error(request,'Invalid credentilas')
            return redirect('user_login')
    else:
        return render(request,'member-login.html')

def user_register(request):
    if request.method =='POST':
        user_email=request.POST['email']
        user_name=request.POST['username']
        phone_number=request.POST['phone_number']
        password=request.POST['password']
        #confirm_password=request.POST['confirm_password']
        #if password==confirm_password:
        if Account.objects.filter(email=user_email).exists():
            messages.error(request,'This is email has already an account!!')
            return redirect('user_register')
             #return render(request,'member-register.html',{'error_msg':"This email have already an account!!"})

        else:
            user=Account.objects.create_user(username=user_name,email=user_email,password=password,phone_number=phone_number)
            user.save()
           # print(password)
            login(request,user)
            print('user reated')
            return redirect('homepage')
        #else:
            #return render(request,'member-register.html',{'error_msg':"Wrong passord"})
    else:
        return render(request,'member-register.html')
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('homepage')
    