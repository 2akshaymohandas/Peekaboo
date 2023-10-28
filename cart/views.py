from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import AddressForm
from accounts.models import Address
from django.views.generic import CreateView
import json


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Coupon




def add_to_cart(request,id):
    
    
    if request.method == 'GET':
        user = request.user if request.user.is_authenticated else None
        print("enerde")
        
        cart, _ = Cart.objects.get_or_create(user=user)
        
        # product = get_object_or_404(Product, pk=id)
        # print(product)
        # selected_size = request.GET.get('selectedsize')
        
        # Check if the selected size is in stock for the product
        product_variant = ProductVariant.objects.filter(pk=id).first()
        product=product_variant.product_name
        print(product_variant)
        if product_variant and product_variant.stock:
            cart_item, item_created = CartItem.objects.get_or_create(user=user,product=product, product_variant=product_variant, cart=cart)
            # Continue with adding the product to the cart
            if not item_created and product_variant.stock :
                cart_item.quantity += 1
            cart_item.save()
            # ... Your existing cart and cart item logic ...
            return JsonResponse({'status': 200, 'message': 'Product added to cart.'})
        else:
            return JsonResponse({'status': 400, 'message': 'Selected size is out of stock.'})
    return redirect('login')
    
    return JsonResponse({'status': 400, 'message': 'Bad request.'})




def update_cart_item(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        cart_item_id = request.POST.get('cart_item_id')
        new_quantity = int(request.POST.get('new_quantity'))

        # Update the cart item quantity logic
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
            if new_quantity > 0:
                cart_item.quantity = new_quantity
                cart_item.save()
                return JsonResponse({'status': 200, 'message': 'Cart item quantity updated.'})
            else:
                return JsonResponse({'status': 400, 'message': 'Invalid quantity.'})
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 404, 'message': 'Cart item not found.'})

    return JsonResponse({'status': 400, 'message': 'Bad request.'})





@login_required(login_url='signin')
def cart(request):
    user = request.user
    try:
        if user: 
            cart,_ = Cart.objects.get_or_create(user=user)
            print(cart)
            
            cart_items = CartItem.objects.filter(user=user)
            if cart_items:
                total = cart.get_total_products()
                coupon = Coupon.objects.all()

                # Check if an offer price is available in the session
                offerprice = request.session.get('offerprice', None)
                if offerprice:
                    sum = offerprice  # Set the offer price as the sum
                    print("OfferPrice")
                else:
                    sum = cart.get_total_price()
                    print("hellowww")


                context = {
                    'cart_items': cart_items,
                    'cart': cart,
                    'sum': sum,
                    'total': total,
                    'coupon' : coupon,
                    'offerprice': offerprice,
                }
                return render(request, 'store/cart.html', context)
            else:
                message = "Your Cart is Empty"
                return render(request, 'store/cart.html', {'message': message})
        else:
            raise Exception("User not authenticated")
    except Exception as e:
        error_message = f"Error occurred: {str(e)}"
        print(error_message)
        return redirect('home')

    return render(request, 'store/cart.html')



def delete_cart_item(request,id):
    cart_item = get_object_or_404(CartItem, pk=id)
    cart_item.delete()
    if 'total' in request.session:
            del request.session['total'] 
    return redirect('cart')





class Add_address(CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'accounts/add_address.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('checkout')
    

class Add_address_user(CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'accounts/add_address.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Address_book')
    



def Address_book(request):
    address = Address.objects.filter(user=request.user)

    context = {
        'address': address,
    }
    return render(request, 'accounts/address.html', context)




def edit_address(request, id):
    product = get_object_or_404(Address, pk=id)
    if request.method == "POST":
        product_form = AddressForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('checkout')
    else:
        product_form = AddressForm(instance=product)

    context = {
        "product_form": product_form
    }
    return render(request, "accounts/edit_address.html", context) 


def edit_addresss_user(request, id):
    product = get_object_or_404(Address, pk=id)
    if request.method == "POST":
        product_form = AddressForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('Address_book')
    else:
        product_form = AddressForm(instance=product)

    context = {
        "product_form": product_form
    }
    return render(request, 'accounts/edit_address.html', context)



def del_address(request, id):
    prod = Address.objects.get(pk=id)
    prod.delete()
    return redirect('checkout')


def del_address_user(request, id):
    prod = Address.objects.get(pk=id)
    prod.delete()
    return redirect('Address_book')


@login_required(login_url='signin')
def checkout(request):
    user = request.user
            
    
    if user: 
            cart,_ = Cart.objects.get_or_create(user=user)
            
            #sum = cart.get_total_price()

            cart_item = CartItem.objects.filter(user=user)

            address = Address.objects.filter(user=user)
            print()

            

            offerprice = request.session.get('offerprice', None)
            total_price = request.session.get('total')
            if offerprice:
                    sum = offerprice
                    print(cart.get_total_price())

            else:
                    sum = total_price if total_price is not None else cart.get_total_price()
                   

                
           
            context = {
        'address'   : address,
        'cart_item' : cart_item,
        'sum': sum,
    }
            
            

    return render(request, "store/checkout.html", context) 



def payment(request):
    print("hh")
    user = request.user
    cart = None  # Initialize cart to None
    cart_items = None  # Initialize cart_items to None
    sum = None  # Initialize sum to None
    total = None  # Initialize total to None
    address = None  # Initialize address to None

    if user: 
        cart, _ = Cart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(user=user)
        print(cart_items)

        if cart_items:
            address_id = request.GET.get('addressId')
            address = Address.objects.get(id=address_id)
            print("kk",address)
            sum = cart.get_total_price()
            

            if 'total' in request.session:
                sum = request.session['total']
            else:
                total = cart.get_total_products()

            offerprice = request.session.get('offerprice', None)
            total_price = request.session.get('total')
            if offerprice:
                    sum = offerprice
            else:
                    sum = total_price if total_price is not None else cart.get_total_price()
               
            

    context = {
        'cart_items': cart_items,
        'cart': cart,
        'sum': sum,
        'total': total,
        'address': address,
    }

    return render(request, "store/payment.html", context)





def filter(request):
    category = Category.objects.all()
    print(category)
    context = {
        'category' : category,
        
    }

    return render (request, 'store/store.html', context)




def apply_coupon(request):
    if request.method == 'POST':
        data = {}
        body = json.loads(request.body)
        coupon_code = body.get('coupon')
        total_price = body.get('total_price')
        if coupon_code:
            request.session['coupon_code'] = coupon_code

        
        try:
            coupon = Coupon.objects.get(coupon_code__iexact=coupon_code, is_expired=False)
        except Coupon.DoesNotExist:
            data['message'] = 'Not a Valid Coupon'
            data['total'] = total_price
        else:
            if coupon.is_expired:
                data['message'] = 'Coupon Already Used'
                data['total'] = total_price
            else:
                minimum_amount = coupon.minimum_amount
                discount_price = coupon.discount_price
                if total_price >= minimum_amount:
                    total_price -= discount_price
                    request.session['total_price'] = total_price
                    request.session['total'] = total_price
                    coupon.is_expired = True
                    coupon.save()
                    print(total_price)
                    data['message'] = f'{coupon.coupon_code} Applied'
                    data['total'] = total_price 
                    print(data)
                else:
                    data['message'] = 'Not a Valid Coupon'
                    data['total'] = total_price
                    print('else')
                    print(data)

        return JsonResponse(data)