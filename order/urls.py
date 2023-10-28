from django.urls import path
from . import views
from . views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
     path('place-order-cod/<int:id>/<str:payment_method>/', PlaceOrderView.as_view(), name='place_order'),

     path('myorders', views.myorders,name="myorders"),
     path('myorder_products/<int:id>/', views.myorder_products,name="myorder_products"),

     
     path('cancel_order/<int:id>/', views.cancel_order,name="cancel_order"),
     path('return_order/<int:id>/', views.return_order,name="return_order"),
    path('confirm_payment_page/<int:id>/',views.confirm_payment,name='confirm_payment_page'),

     # path('complete_payment',views.complete_payment,name="complete_payment"),
     path('thanks_page',views.thanks_page,name="thanks_page"),



    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)