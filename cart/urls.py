from django.urls import path
from . import views

urlpatterns = [
    # cart items
    path('',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('remove_cart/<int:product_id>/',views.remove_cart,name='remove_cart'),
    path('decrement_quantity/',views.decrement_quantity,name='decrement_quantity'),
    path('increment_cart/',views.increment_cart,name='increment_cart'),
    path('remove_cart_item/',views.remove_cart_item,name='remove_cart_item'),
    
    # whislist

    
    path('Whislist/',views.Whislist,name='Whislist'),
    path('AddWhishlist/',views.AddWhishlist,name='AddWhishlist'),
    path('removeWish <int:id>/',views.removeWish,name='removeWish'),


    # coupons
    path('viewcoupon',views.viewcoupon,name='viewcoupon'),
    path('apply_coupon',views.apply_coupon,name='apply_coupon'),
    path('delete_coupon',views.delete_coupon,name='delete_coupon'),



    path('checkout/',views.checkout,name='checkout'),
]
