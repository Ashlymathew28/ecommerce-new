from django.shortcuts import render,redirect
from django.template import context
from accounts.models import Account
from django.utils.text import slugify
from store.models import Product
from django.contrib import messages
from category.models import category
# Create your views here.

def admin_home(request):
    print('haiiiii')
    return render(request,'admin/admin-home.html')

#for seeing userlist for admin
def admin_userlist(request):
    print('>>>>>>>>>>')
    new=Account.objects.all()
    
    #context={'userlist':new}
    #print(context)
    return render(request,'admin/admin-user.html',{'new':new})

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
    user=Account.objects.get(id=id)
    user.blocked=False
    user.save()
    print(user)
    return redirect('admin_userlist')

def admin_category(request):
    print('}}}}}}}}}}}}}}')
    new=category.objects.all()
    return render(request,'admin/admin-category.html',{'new':new})

#adding category

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


def admin_productlist(request):
    product=Product.objects.all()
    return render(request,'admin/admin-productlist.html',{'product':product})

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
        product=Product()
        product.slug=slugify(product_name)
        product.product_name=product_name
        product.description=description
        product.price=price
        product.category_id=cat
        product.stock=stock
        if 'Image' in request.FILES:
              product.images=request.FILES['Image']
        product.save()
        return redirect('admin_productlist')


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
        image=request.FILES.get('Image')
        cat=request.POST.get('category')
        stock=request.POST.get('stock')

        product.product_name=product_name
        product.description=description
        product.price=price
        product.images=image
        product.stock=stock
        product.save()
        return redirect('admin_productlist')


def remove_product(request,id):
    remove=Product.objects.get(id=id).delete() 
    return redirect('admin_productlist')