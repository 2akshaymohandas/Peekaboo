from django.contrib import admin
from django.urls import path
from. import views

urlpatterns = [
    
    path('', views.home, name="home"),
    path('store', views.store, name="store"),

    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),

    path('otp_login', views.otp_login, name="otp_login"),
    path('verify_code', views.verify_code, name="verify_code"),

    path('product/<slug:slug>/', views.product_details, name="product_details"),

    path('store/<slug:category_slug>/', views.store, name="products_by_category"),

    path('dashboard', views.dashboard, name="dashboard"),

    path('forgotPassword', views.forgotPassword,name="forgotPassword"),
    path('forgotPassword_otp', views.forgotPassword_otp,name="forgotPassword_otp"),
    path('resetPassword', views.resetPassword,name="resetPassword"),

    path('edit_address', views.edit_address,name="edit_address"),

    path('men', views.men,name="men"),
    path('women', views.women,name="women"),

    

    path('wishlist', views.wishlist,name="wishlist"),
    path('add_to_wishlist/<int:id>/', views.add_to_wishlist,name="add_to_wishlist"),
    path('remove_from_wishlist/<int:id>/', views.remove_from_wishlist,name="remove_from_wishlist"),

    path('price_sort', views.price_sort, name='price_sort'),
    

    
]