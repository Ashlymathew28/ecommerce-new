from django.urls import path
from . import views

urlpatterns = [
    path('admin_home/',views.admin_home,name='admin_home'),
    path('admin_userlist/',views. admin_userlist,name='admin_userlist'),
    path('admin_category/',views. admin_category,name='admin_category'),
    path('admin_block <int:id>/ ',views. admin_block,name='admin_block'),
    path('admin_unblock <int:id>/',views. admin_unblock,name='admin_unblock'),
    path('admin_productlist/',views. admin_productlist,name='admin_productlist'),
    path('admin_addproduct/',views. admin_addproduct,name='admin_addproduct'),
    path('edit_product <int:id>/',views. edit_product,name='edit_product'),
    path('remove_product <int:id>',views. remove_product,name='remove_product'),

    path('admin_addcategory/',views. admin_addcategory,name='admin_addcategory'),
    path('delete_category <int:id>/',views. delete_category,name='delete_category'),
    path('edit_category <int:id>/',views.edit_category,name='edit_category'),
    path('update_category <int:id>/',views. update_category,name='update_category'),

]