from django.urls import path
from . import views

urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('payments',views.payments,name='payments'),
    path('proceed_to_pay',views.proceed_to_pay,name='proceed_to_pay'),
]
