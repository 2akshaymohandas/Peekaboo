from django.contrib import admin
from django.urls import path
from. import views

urlpatterns = [
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),

    path('sales_report', views.sales_report,name="sales_report"),
    path('sales_report_by_product/<int:id>/', views.sales_report_by_product,name="sales_report_by_product"),
    path('sales_date', views.sales_date,name="sales_date"),

    path('user/', views.user, name='user'),
    
    path('category/', views.category, name='category'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/<int:id>/', views.edit_category,name="edit_category"),
    path('del_category/<int:id>/', views.del_category,name="del_category"),

    path('category_offer_manage/<str:category_name>/', views.category_offer_manage, name='category_offer_manage'),

    path('brand', views.brand,name="brand"),
    path('add_brand', views.add_brand,name="add_brand"),
    path('edit_brand<int:id>/', views.edit_brand,name="edit_brand"),
    path('del_brand<int:id>/', views.del_brand,name="del_brand"),
    path('product_variant', views.product_variant, name="product_variant"),
    path('products', views.products,name="products"),
    path('add_product', views.add_product,name="add_product"),
    path('edit_product/<int:id>/', views.edit_product,name="edit_product"),
    path('del_product/<int:id>/', views.del_product,name="del_product"),

    path('product_variant', views.product_variant, name="product_variant"),
    path('add_product_variant', views.add_product_variant,name="add_product_variant"),
    path('del_product_variant/<int:id>/', views.del_product_variant,name="del_product_variant"),
    path('edit_product_variant/<int:id>/', views.edit_product_variant,name="edit_product_variant"),

    path('size', views.size,name="size"),
    path('add_size', views.add_size,name="add_size"),
    path('del_size/<int:id>/', views.del_size,name="del_size"),

    path('unblock_user/<int:id>', views.unblock_user,name="unblock_user"),
    path('block_user/<int:id>/', views.block_user,name="block_user"),

    path('orders', views.orders,name="orders"),
    path('order_products/<int:id>/', views.order_products,name="order_products"),   
    path('edit_order/<int:id>/', views.edit_order,name="edit_order"),
    path('search_order', views.search_order,name="search_order"), 


    path('coupon_manage', views.coupon_manage,name="coupon_manage"),   
    path('add_coupon', views.add_coupon,name="add_coupon"),   
    path('del_coupon/<int:id>/', views.del_coupon,name="del_coupon"),   
    path('edit_coupon/<int:id>/', views.edit_coupon,name="edit_coupon"), 

    path('product_offer_manage', views.product_offer_manage,name="product_offer_manage"), 
    path('add_offer', views.add_offer,name="add_offer"), 
    path('del_pro_offer/<int:id>/', views.del_pro_offer,name="del_pro_offer"), 

    

    
    

    




]