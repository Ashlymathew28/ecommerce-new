from django.urls import path
from . import views

urlpatterns = [
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),

    # banners
    path('banners/',views.banners,name='banners'),
    path('addBanner/',views.addBanner,name='addBanner'),
    path('editBanner <int:id>/',views.editBanner,name='editBanner'),
    path('removeBanner <int:id>/',views.removeBanner,name='removeBanner'),

# users
    path('admin_userlist/',views. admin_userlist,name='admin_userlist'),
    path('admin_category/',views. admin_category,name='admin_category'),
    path('admin_block <int:id>/ ',views. admin_block,name='admin_block'),
    path('admin_unblock <int:id>/',views. admin_unblock,name='admin_unblock'),

# product

    path('admin_productlist/',views. admin_productlist,name='admin_productlist'),
    path('prodsearch/',views. prodsearch,name='prodsearch'),
    path('admin_addproduct/',views. admin_addproduct,name='admin_addproduct'),
    path('edit_product <int:id>/',views. edit_product,name='edit_product'),
    path('remove_product <int:id>',views. remove_product,name='remove_product'),
    path('addproduct_Offer <int:id>',views. addproduct_Offer,name='addproduct_Offer'),
    path('edit_prodOffer <int:id>',views. edit_prodOffer,name='edit_prodOffer'),
    path('remove_productOffer/',views. remove_productOffer,name='remove_productOffer'),

# category

    path('admin_addcategory/',views. admin_addcategory,name='admin_addcategory'),
    path('delete_category/',views. delete_category,name='delete_category'),
    path('edit_category <int:id>/',views.edit_category,name='edit_category'),
    path('update_category <int:id>/',views. update_category,name='update_category'),
    path('add_catOffer <int:id>/',views. add_catOffer,name='add_catOffer'),
    path('edit_catOffer <int:id>/',views. edit_catOffer,name='edit_catOffer'),
    path('remove_catOffer/',views. remove_catOffer,name='remove_catOffer'),

# orders
    path('admin_orderlist/',views.admin_orderlist,name='admin_orderlist'),
    path('editStatus/',views.editStatus,name='editStatus'),
    path('viewDetails <int:id>/',views.viewDetails,name='viewDetails'),

# salesReport
    path('salesReport/',views.salesReport,name='salesReport'),
    path('genereateSalesreport/',views.genereateSalesreport.as_view(),name='genereateSalesreport'),
    path('by_date/',views.by_date,name='by_date'),
    path('by_month/',views.by_month,name='by_month'),


# coupons

    path('admin_coupons/',views.admin_coupons,name='admin_coupons'),
    path('admin_addcoupon/',views.admin_addcoupon,name='admin_addcoupon'),
    path('RemoveCoupon/<int:id>/',views.RemoveCoupon,name='RemoveCoupon'),

]