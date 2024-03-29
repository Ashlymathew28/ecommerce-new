from django.urls import path
from . import views

urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('payments',views.payments,name='payments'),
    path('proceed_to_pay',views.proceed_to_pay,name='proceed_to_pay'),
    path('order_cancel',views.order_cancel,name='order_cancel'),
    path('order_return',views.order_return,name='order_return'),
    path('genericinvoice/<int:id>/',views.generateInvoice.as_view(),name='generateinvoice'),
]
