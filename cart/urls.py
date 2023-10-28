from django.urls import path
from . import views
from . views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
     path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
     path('update_cart_item', views.update_cart_item, name='update_cart_item'),
     path('cart/', views.cart, name='cart'),

     path('delete_cart_item/<int:id>/', views.delete_cart_item,name="delete_cart_item"),
     path('add_address', Add_address.as_view(),name="Add_address"),
     path('Add_address_user', Add_address_user.as_view(),name="Add_address_user"),
     path('checkout', views.checkout,name="checkout"),


     path('payment', views.payment, name="payment"),

     path('Address_book', views.Address_book,name="Address_book"),
     path('edit_address/<int:id>/', views.edit_address,name="edit_address"),
     path('edit_addresss_user/<int:id>/', views.edit_addresss_user,name="edit_addresss_user"),

     path('del_address/<int:id>/', views.del_address,name="del_address"),
     path('del_address_user/<int:id>/', views.del_address_user,name="del_address_user"),
     path('filter', views.filter, name="filter"), 
     path('apply_coupon', views.apply_coupon, name="apply_coupon"),

     

     


    
]