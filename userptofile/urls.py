from django.urls import path
from . import views

urlpatterns = [
    path('userdetails/',views.userdetails,name='userdetails'),
    path('useraddress/',views.useraddress,name='useraddress'),
    path('userAddAddress/',views.userAddAddress,name='userAddAddress'),
    path('my_order',views.my_order,name='my_order'),
    path('orderDetails <int:id>/', views.orderDetails,name='orderDetails'),
]