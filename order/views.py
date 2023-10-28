from typing import Any
from django.views import View
from django.shortcuts import render, redirect
from .models import *
from accounts.models import *
from products.models import *
from cart.models import *
from .models import *
from django.http import JsonResponse
#from .forms import *
from cart.views import *
import datetime
from django.urls import reverse
import decimal
import uuid
from django.utils import timezone
import razorpay
from django.conf import settings


def myorders(request):
    order = OrderProduct.objects.filter(user=request.user).order_by("-created_at")
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    
    context = {
        'order': order,
        'orders': orders,
        
    }
    return render(request, 'accounts/orders.html', context)


def myorder_products(request, id):
    orders = Order.objects.get(pk=id)
    
    myorder = OrderProduct.objects.filter(order=orders)
    add = orders.address

    context = {
        'orders': orders,
        'myorder':myorder,
        'add': add,
    }
    return render(request, 'myorders_products.html', context) 



def cancel_order(request,id):
    print(id)
    if request.method == "POST":
        cancellation_reason = request.POST.get('cancellation_reason')
        try:
        
            order = get_object_or_404(Order, pk=id, user=request.user)
            orders = OrderProduct.objects.filter(order=order)
            order.status = 'Cancelled'
            order.cancellation_reason = cancellation_reason
            order.save()
            if order.status == 'Cancelled':
                for product in orders:
                    product.variation.stock += product.quantity
                    product.variation.save()
                

        #     if order.payment.payment_method =='Razorpay':
        #         wallet, _ =Wallet.objects.get_or_create(user=request.user)
        #         refund_amount=decimal.Decimal(order.order_total)
        #         wallet.balance += refund_amount
        #         wallet.save()

        except Order.DoesNotExist:
            pass
    return redirect("myorders")
            




def return_order(request,id):
    print(id)
    if request.method=="POST":
        return_reason=request.POST.get('return_reason')
        try:
            order = get_object_or_404(Order, pk=id, user= request.user)
            order.status='Return'
            order.return_reason = return_reason
            
            order.save()
            if order.payment.payment_method == 'Razorpay' or 'COD':
                wallet, _ = Wallet.objects.get_or_create(user=request.user)
                orders = OrderProduct.objects.filter(order=order)
                refund_amount = decimal.Decimal(order.order_total)
                wallet.balance += refund_amount
                wallet.save()
                print(wallet.balance)
                if order.status == 'Return':
                    for product in orders:
                        product.variation.stock += product.quantity
                        product.variation.save()

        except Order.DoesNotExist:
            pass
    return redirect('myorders')






def place_order(request,id,payment_method):
        if payment_method =="Razorpay":
            print("razor")


            #cart_items.delete()
            if 'total' in request.session:
                del request.session['total']

            return redirect ("thanks_page")
        else:

        
            user=request.user
            pymentid=str(uuid.uuid4()) 
            cart= Cart.objects.get(user=user)
            
            if 'total' in request.session:
                    total = request.session['total']
                    
            else:
                    total = cart.get_total_price()
                    
            address=Address.objects.get(pk=id)


            cart_items = CartItem.objects.filter(user=request.user)
            pyment=Payment.objects.create(user=user,payment_id=pymentid,payment_method="COD",amount_paid=total,status="pending")

            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            unique_id = str(uuid.uuid4().fields[-1])[:8]
            order_number = f'{timestamp}-{unique_id}'
            order = Order.objects.create(
                    user=user,
                    payment=pyment,
                    address=address,
                    order_number=order_number,  
                    order_note='',  
                    order_total=total,  
                    tax=0.0,  
                    status='New',  
                    ip='...', 
                    is_ordered=False  
            )


            for cart_item in cart_items:
                
                    product_price=cart_item.product.price
                    OrderProduct.objects.create(
                    order=order,
                    payment=pyment,
                    user=user,
                    product=cart_item.product,
                    variation=cart_item.product_variant ,
                    quantity=cart_item.quantity,                       
                    product_price=product_price,
                    ordered=False
                    )

            #cart_items.delete()
            if 'total' in request.session:
                del request.session['total']

            return redirect ("thanks_page")
        



class PlaceOrderView(View):

    def get(self, request, id,payment_method):
        # Retrieve user, address, and other necessary data from the request
        user=request.user
        pymentid=str(uuid.uuid4()) 
        cart= Cart.objects.get(user=user)
        
        if 'total' in request.session:
                total = request.session['total']
                
        else:
                total = cart.get_total_price()

        
                
        address=Address.objects.get(pk=id)


        cart_items = CartItem.objects.filter(user=request.user)
        pyment=Payment.objects.create(user=user,payment_id=pymentid,payment_method=payment_method,amount_paid=total,status="pending")

        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        unique_id = str(uuid.uuid4().fields[-1])[:8]
        order_number = f'{timestamp}-{unique_id}'
        order = Order.objects.create(
                user=user,
                payment=pyment,
                address=address,
                order_number=order_number,  
                order_note='',  
                order_total=total,  
                tax=0.0,  
                status='New',  
                ip='...', 
                is_ordered=False  
        )



        for cart_item in cart_items:
            
                product_price=cart_item.product.price
                OrderProduct.objects.create(
                order=order,
                payment=pyment,
                user=user,
                product=cart_item.product,
                variation=cart_item.product_variant ,
                quantity=cart_item.quantity,                       
                product_price=product_price,
                ordered=False
                )
                product = cart_item.product_variant
                product.stock -= cart_item.quantity
                product.save()

        cart_items.delete()
        if 'offerprice' in request.session:
            del request.session['offerprice']
        if 'total' in request.session:
            del request.session['total']
            
        return redirect ("thanks_page")



        
def confirm_payment(request,id):
    print("hh")
    user = request.user
    cart = None 
    cart_items = None 
    sum = None
    total = None 
    address = None 

    if user: 
        cart, _ = Cart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(user=user)
        print(cart_items)

        if cart_items:
            address = Address.objects.get(id=id)
            print("kk",address)
            sum = int(cart.get_total_price())
            

            if 'total' in request.session:
                sum = request.session['total']
            else:
                total = cart.get_total_products()

            client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
   
            payment = client.order.create({ "amount": sum*100, "currency": "INR", "receipt": "order_rcptid_11" })
        
               
            

    context = {
        'cart_items': cart_items,
        'cart': cart,
        'sum': sum,
        'total': total,
        'address': address,
        'payment':payment,
    }

    return render(request, "store/confirm.html", context)



def thanks_page(request):
     
     order = Order.objects.filter(user=request.user).latest('created_at')
     
     context = {
          "order": order,
          
     }
     return render (request, 'accounts/order-success.html', context)

        
     





















                        


# def complete_payment(request):
#         id = request.GET.get('id')
#         payment_id = request.GET.get('payment_id')
#         payment_method = Payment.objects.filter(user=request.user)
#         amount = request.GET.get('amount')
#         if payment_method == "razorpay":
#                 amount = float(amount)/100
#         order_number = request.GET.get('order_number')
#         address_id=request.GET.get('address_id')

#         address = Address.objects.get(id=address_id)

#         context = {
#                 'id': id,
#                 'payment_id': payment_id,
#                 'amount': amount,
#                 'order_number': order_number,
#                 'address': address,
#                 }
#         return render(request, "store/order-complete.html", context)
