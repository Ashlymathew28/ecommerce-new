from django.shortcuts import render,redirect
from django.template import context
from accounts.models import Account
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

from django.contrib.auth import authenticate,login,logout
from django.utils.text import slugify
from store.models import Product
from django.contrib import messages
from category.models import category
from orders.models import *
from django.http import JsonResponse
from offers.models import Coupon,product_offer,cat_offer
# Create your views here.

def admin_login(request):
    if request.method == 'POST':
        email=request.POST.get('adminname')
        password=request.POST.get('adminpassword')
        user=authenticate(email=email,password=password)
        # print(user.is_admin)
        if user is not None:
            login(request,user)
            if request.user.is_superuser == True:
                return redirect('admin_home')
            else:
                messages.error(request,'Your email or password is Incorrect!!')
                return redirect('admin_login')
        else:
            messages.error(request,'You are not an admin!!!')
            return redirect('admin_login') 

    return render(request,'admin/admin-login.html')
        

@login_required(login_url='admin_login')
def admin_home(request):
    if request.user.is_superuser==True:
       print('haiiiii')
        
       return render(request,'admin/admin-home.html')
    return redirect('admin_login')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

#for seeing userlist for admin
@login_required(login_url='admin_login')
def admin_userlist(request):
    print('>>>>>>>>>>')
    new=Account.objects.all()
    paginator=Paginator(new,2)
    page=request.GET.get('page')
    paged_new=paginator.get_page(page)
    #context={'userlist':new}
    #print(context)
    print(paged_new)
    return render(request,'admin/admin-user.html',{'new':paged_new})

#for blocking user
def admin_block(request,id):
    print('blocked')
    user=Account.objects.get(id=id)
    user.blocked=True
    user.save()
    print(user.blocked)
    return redirect('admin_userlist')


#for unblocking user
def admin_unblock(request,id):
    print('unblocked')
    users=Account.objects.get(id=id)
    users.blocked=False
    users.save()
    print(users)
    return redirect('admin_userlist')

#to see the categorylist
@login_required(login_url='admin_login')
def admin_category(request):
    print('}}}}}}}}}}}}}}')
    new=category.objects.all()
    
    return render(request,'admin/admin-category.html',{'new':new})

#adding category
@login_required(login_url='admin_login')
def admin_addcategory(request):
    if request.method == 'GET':
       return render(request,'admin/admin-addcategory.html')
    else:
        if request.method == 'POST':
           print('post')
           name=request.POST['catname']
           description=request.POST['catdescription']
           image=request.FILES['Image']
           
           cat=category()
           cat.category_name=name
           cat.slug=slugify(name)
           cat.description=description
           if image in request.FILES:
              cat.category_image=request.FILES['Image']
           cat.save()
           return redirect('admin_category')

def delete_category(request,id):
    remove=category.objects.get(id=id).delete()
    return redirect('admin_category')

def edit_category(request,id):
    cat=category.objects.get(id=id)
    return render(request,'admin/admin-editcategory.html',{'cat':cat})

#saving edited product to databse
@login_required(login_url='admin_login')
def update_category(request,id):
    if request.method == 'POST':
       Category=category.objects.get(id=id)
       Category_name=request.POST.get('catname')
       description=request.POST.get('catedescription')
       image=request.FILES.get('Image')
       Category.category_name=Category_name
       Category.category_image=image
       Category.description=description
       Category.save()
       messages.info(request,"Category updated")
    return redirect('admin_category')

# for seeing productlist
@login_required(login_url='admin_login')
def admin_productlist(request):
    product=Product.objects.all()
    paginator=Paginator(product,4)
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)
    return render(request,'admin/admin-productlist.html',{'product':paged_products})


@login_required(login_url='admin_login')
def admin_addproduct(request):
    if request.method == 'GET':
       cat=category.objects.all()
       
       return render(request,'admin/admin-product.html',{'cat':cat})
    
    else:
        product_name=request.POST['productname']
        description=request.POST['description']
        price=request.POST['price']
        # image=request.FILES['Image']
        cat=request.POST['category']
        print(cat,'//////////////')
        stock=request.POST['stock']
        slug=slugify(product_name)
        slug_compare=Product.objects.filter(prod_slug=slug)
        if slug == slug_compare:
            return redirect('admin_add')
        product=Product() 
        product.prod_slug=slugify(product_name)
        product.product_name=product_name
        product.description=description
        product.price=price
        product.user_price=price
        product.category_id=cat
        product.stock=stock
        if 'Image' in request.FILES:
              product.images=request.FILES['Image']
        if 'Image1' in request.FILES:
              product.image1=request.FILES['Image1']
        if 'Image2' in request.FILES:
              product.image2=request.FILES['Image2']
        product.save()
        return redirect('admin_productlist')



@login_required(login_url='admin_login')
def edit_product(request,id):
    if request.method == 'GET':
       prod=Product.objects.get(id=id)
       cat=category.objects.all()
       context={
        'prod':prod,
        'cat':cat
       }
       return render(request,'admin/admin-editproduct.html',context)
    else:
        product=Product.objects.get(id=id)
        product_name=request.POST.get('productname')
        description=request.POST.get('description')
        price=request.POST.get('price')     
        images=request.FILES.get('Image')
        image1=request.FILES.get('Image1')
        image2=request.FILES.get('Image2')
        cat=request.POST.get('category')
        stock=request.POST.get('stock')

        product.product_name=product_name
        product.description=description
        product.price=price
        product.user_price=price
        product.images=images
        product.image1=image1
        product.image2=image2
        product.stock=stock
        product.save()
        return redirect('admin_productlist')


def remove_product(request,id):
    remove=Product.objects.get(id=id).delete() 
    return redirect('admin_productlist')

# for adding product offer
def addproduct_Offer(request,id):
    if request.method == 'POST':
        prod_offer=product_offer()
        prod_offer.name=request.POST.get('productofferName')
        prod_offer.offer=request.POST.get('offer')
        prod_offer.offer_type=request.POST.get('offerType')
    
        prod_offer.product_id=id
        prod_offer.save()
        offer_price=(prod_offer.product.price)-(prod_offer.product.price*(int(prod_offer.offer)/100))
        prod_offer.product.p_offer=offer_price
        print(offer_price)
        print("product offer kandu pidichu kutta ")
        print(prod_offer.product.p_offer)
        prod_offer.product.save()

        if prod_offer.product.p_offer < 1 and prod_offer.product.cat_offer < 1:
            prod_offer.product.user_price = prod_offer.product.price

        elif prod_offer.product.p_offer < prod_offer.product.cat_offer and prod_offer.product.p_offer > 1:
            prod_offer.product.user_price = prod_offer.product.p_offer
        
        elif prod_offer.product.cat_offer < prod_offer.product.p_offer and prod_offer.product.cat_offer > 1:
            prod_offer.product.user_price = prod_offer.product.cat_offer

        elif prod_offer.product.cat_offer > 1 and prod_offer.product.p_offer == 0:
            prod_offer.product.user_price =prod_offer.product.cat_offer
        
        elif prod_offer.product.p_offer > 1 and prod_offer.product.cat_offer == 0:
            prod_offer.product.user_price = prod_offer.product.p_offer
        
        else:
            prod_offer.product.user_price = prod_offer.product.cat_offer
        
        prod_offer.product.save()


        return redirect('admin_productlist')

    else:
        product=Product.objects.get(id=id)
        return render(request,'admin/admin-prodOffer.html',{'product':product})
    
# for editing product Offer
def edit_prodOffer(request,id):
    
    if request.method =='POST':
        print(id)
        prod_offer=product_offer.objects.get(id=id)
        print("editttttttt")
        print(prod_offer)
        prod_offer.name=request.POST.get('productofferName')
        prod_offer.offer=request.POST.get('offer')
        prod_offer.offer_type=request.POST.get('offerType')
    
        # prod_offer.product_id=id
        prod_offer.save()
        offer_price=(prod_offer.product.price)-(prod_offer.product.price*(int(prod_offer.offer)/100))
        prod_offer.product.p_offer=offer_price
        print(offer_price)
        print("product offer kandu pidichu kutta ")
        print(prod_offer.product.p_offer)
        prod_offer.product.save()

        if prod_offer.product.p_offer < 1 and prod_offer.product.cat_offer < 1:
            prod_offer.product.user_price = prod_offer.product.price

        elif prod_offer.product.p_offer < prod_offer.product.cat_offer and prod_offer.product.p_offer > 1:
            prod_offer.product.user_price = prod_offer.product.p_offer
        
        elif prod_offer.product.cat_offer < prod_offer.product.p_offer and prod_offer.product.cat_offer > 1:
            prod_offer.product.user_price = prod_offer.product.cat_offer

        elif prod_offer.product.cat_offer > 1 and prod_offer.product.p_offer == 0:
            prod_offer.product.user_price =prod_offer.product.cat_offer
        
        elif prod_offer.product.p_offer > 1 and prod_offer.product.cat_offer == 0:
            prod_offer.product.user_price = prod_offer.product.p_offer
        
        else:
            prod_offer.product.user_price = prod_offer.product.cat_offer
        
        prod_offer.product.save()


        return redirect('admin_productlist')

    else:
        print(id)
        offer=product_offer.objects.get(product_id=id)
        print(offer)
        return render(request,'admin/edit_productOffer.html',{'offer':offer})


# removing prodOffer
def remove_productOffer(request):
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("keriiii")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    id=request.GET.get('id')
    print(id)
    prod_offer=product_offer.objects.get(product_id=id)
    prod_offer.product.p_offer = 0
    prod_offer.product.save()
    
    if prod_offer.product.p_offer < 1 and prod_offer.product.cat_offer < 1:
        prod_offer.product.user_price = prod_offer.product.price

    elif prod_offer.product.p_offer < prod_offer.product.cat_offer and prod_offer.product.p_offer > 1:
        prod_offer.product.user_price = prod_offer.product.p_offer
        
    elif prod_offer.product.cat_offer < prod_offer.product.p_offer and prod_offer.product.cat_offer > 1:
        prod_offer.product.user_price = prod_offer.product.cat_offer

    elif prod_offer.product.cat_offer > 1 and prod_offer.product.p_offer == 0:
        prod_offer.product.user_price =prod_offer.product.cat_offer
    
    elif prod_offer.product.p_offer > 1 and prod_offer.product.cat_offer == 0:
        prod_offer.product.user_price = prod_offer.product.p_offer
        
    else:
        prod_offer.product.user_price = prod_offer.product.cat_offer
        
    prod_offer.product.save()
    prod_offer.delete()

    return JsonResponse({'status':'true'})


def add_catOffer(request,id):
    if request.method =='POST':
        catedory_offer=cat_offer()
        catedory_offer.name=request.POST.get('productofferName')
        catedory_offer.offer=request.POST.get('offer')
        catedory_offer.offer_type=request.POST.get('offerType')
      
        catedory_offer.category_id=id
        catedory_offer.save()
        print("category offer save aayito")
        catedory_offer.category.c_offer=True
        catedory_offer.category.save()

        prod=Product.objects.filter(category_id=id)

        for i in prod:
            i.cat_offer=i.price-(i.price*(int(catedory_offer.offer)/100))
            i.save()

            if i.p_offer < 1 and i.cat_offer < 1:
                i.user_price = i.price

            elif i.p_offer < i.cat_offer and i.p_offer > 1:
                i.user_price = i.p_offer
        
            elif i.cat_offer < i.p_offer and i.cat_offer > 1:
                i.user_price = i.cat_offer

            elif i.cat_offer > 1 and i.p_offer == 0:
                i.user_price =i.cat_offer
        
            elif i.p_offer > 1 and i.cat_offer == 0:
                i.user_price = i.p_offer
        
            else:
                i.user_price = i.cat_offer
                print("category offer calculate aaki")
            i.save()
        return redirect('admin_category')

    else:
        Category=category.objects.get(id=id)
        return render(request,'admin/admin-CatOffer.html',{'Category':Category})

# for editing cat offer
def edit_catOffer(request,id):
    if request.method =='POST':
        catedory_offer=cat_offer.objects.get(id=id)
        catedory_offer.name=request.POST.get('productofferName')
        catedory_offer.offer=request.POST.get('offer')
        catedory_offer.offer_type=request.POST.get('offerType')
      
        
        catedory_offer.save()
        c_id=catedory_offer.category_id
        print("iddddddddddddddddd",c_id)
        print("category offer save aayito")
        catedory_offer.category.c_offer=True
        catedory_offer.category.save()

        prod=Product.objects.filter(category_id=c_id)
        print("forrrrrrrrrrrrrrrrr")
        print(prod)
        for i in prod:
            print("proddddddddddddddddddd")
            i.cat_offer=i.price-(i.price*(int(float(catedory_offer.offer))/100))
            i.save()

            if i.p_offer < 1 and i.cat_offer < 1:
                i.user_price = i.price

            elif i.p_offer < i.cat_offer and i.p_offer > 1:
                i.user_price = i.p_offer
        
            elif i.cat_offer < i.p_offer and i.cat_offer > 1:
                i.user_price = i.cat_offer

            elif i.cat_offer > 1 and i.p_offer == 0:
                i.user_price =i.cat_offer
        
            elif i.p_offer > 1 and i.cat_offer == 0:
                i.user_price = i.p_offer
        
            else:
                i.user_price = i.cat_offer
                print("category offer calculate aaki")
            i.save()
        return redirect('admin_category')
        

    else:
        cate_offer=cat_offer.objects.get(category_id=id)
        return render(request,'admin/editCatOffer.html',{'cate_offer':cate_offer})


# for removing cat offer
def remove_catOffer(request):
    pass

#for seeing coupons 
def admin_coupons(request):
    coupon=Coupon.objects.all()
    return render(request,'admin/admin-coupons.html',{'coupon':coupon})

def admin_addcoupon(request):
    if request.method == 'POST':
       coupon=Coupon()
       coupon.coupon_name= request.POST.get('couponName')
       coupon.coupon_code = request.POST.get('code')
       coupon. discount=request.POST.get('discount')
       coupon.valid_from=request.POST.get('validFrom')
       coupon.valid_to=request.POST.get('validTo')
       coupon.save()
       return redirect('admin_coupons')

    else:    
        return render(request,'admin/admin_addcoupon.html')

# for seeing order list
def admin_orderlist(request):
    orderlist = OrderProduct.objects.all()
    paginator=Paginator(orderlist,10)
    page=request.GET.get('page')
    paged_orderlist=paginator.get_page(page)

    return render(request,'admin/orderList.html',{'orderlist':paged_orderlist} )

