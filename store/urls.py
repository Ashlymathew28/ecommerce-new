from django.urls import path
from . import views

urlpatterns = [
    path('user_shop',views.user_shop,name='user_shop'),
    path('<slug:category_slug>',views.user_shop,name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/ ',views.product_detail,name='product_detail'),
]
  