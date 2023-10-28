from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from products . models import *
from .forms import VerifyForm, PhonecheckForm
#from . import verify
from django.shortcuts import get_object_or_404
import json
from django.http import JsonResponse
from . import verify
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.models import Session
import json
from django.core.exceptions import ObjectDoesNotExist
import decimal
from django import forms
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.cache import cache_control



@cache_control(private=True, no_cache=True, no_store=True, must_revalidate=True)
@never_cache
def home(request):

    products = Product.objects.all().filter(is_available = True)
    
    context =  {
        'products'     : products
        }

    return render(request,'store/home.html', context )




def signup(request):

    email = request.session.get('email')
    if email:
        return redirect('home')
    if request.method == "POST":
        print("NO way")
        email = request.POST['email']
        name = request.POST['name']
        phone = request.POST['phone']
        if phone:  # Ensure the phone number is not empty
            if len(phone) == 10 and phone.isdigit():  # Check if the phone number is exactly 10 digits and consists only of numeric characters
                phone = '+91' + phone  # Add the '+91' prefix to the phone number

        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        
        if pass1 == pass2:
            if CustomUser.objects.filter(email=email).exists():
                messages.info(request,"User already exists")
                return redirect('signup')
            else:
                user = CustomUser.objects.create_user(email=email, name=name, phone_number=phone, password=pass1)
                Wallet.objects.create(user=user, balance=0)
                
                user.save()

                subject = 'Welcome to our website'
                from_email = 'fly2akshay@gmail.com'
                to_email = user.email

                html_message = render_to_string('accounts/welcome_email.html')
                plain_message = strip_tags(html_message)

                send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

                return redirect("signin")
        else:
            messages.info(request, 'Password do not match')
            return redirect('signup')

    return render(request,"accounts/signup.html")




@cache_control(private=True, no_cache=True, no_store=True, must_revalidate=True)
@never_cache
def signin(request):
    email = request.session.get('email')
    if email:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email= email, password= password)
        

        if user is not None:
            auth.login(request, user)
            #messages.success(request,'You are now logged in.')
            return redirect('home')
        
        else:
            messages.error(request,'Invalid Login credentials')
            return redirect('signin')
                

    return render (request, 'accounts/signin.html')

@login_required(login_url = 'signin')
def signout(request):
    auth.logout(request)
    request.session.flush()
    messages.success(request, 'You are logged out.')
    return redirect('home')



def store(request,category_slug = None,):

    categories = None
    Products   = None

    if category_slug != None:
        categories   = get_object_or_404(Category, slug = category_slug)
        products     = Product.objects.filter(category=categories, is_available = True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()


    context =  {
        'products'     : products,
        'product_count': product_count,
        
        }

    return render(request, 'store/store.html', context)





def product_details(request, slug):

    pro = get_object_or_404(Product, slug=slug)
    print("hbhg")
    print(pro)
    product_varient=ProductVariant.objects.filter(product_name=pro)

    offer = Product_offer.objects.filter(product__slug=slug)
    

    total_discount = 0  # Initialize the total discount to 0

    for offer in offer:
        total_discount += offer.discount

    offerprice = pro.price - total_discount

    if total_discount != 0:
        request.session['offerprice'] = offerprice

    image = ProductImage.objects.filter(product_name=pro)


    


    return render(request, 'store/product_detail.html', {'pro': pro,
                                                         'prodvar':product_varient,
                                                         'offer': offer,
                                                         'offerprice':offerprice,
                                                         'image': image}
                                                         )


def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            phone = request.session.get('phone_number')
            print(phone)

            if verify.check(phone, code):
                try:
                    user = CustomUser.objects.get(phone_number=phone)
                    # Perform any additional checks if needed
                    if user.is_active and not user.is_superuser:
                        login(request, user)
                        return redirect('home')
                    else:
                        return redirect('inactive_user')  # Redirect to a page for inactive users
                except CustomUser.DoesNotExist:
                    return redirect('user_not_found')  # Redirect to a page for users not found
            else:
                print("error")  

    else:
        form = VerifyForm()
    return render(request, 'accounts/verify_code.html', {'form': form})




#OTP_COMMENTED
# def otp_login(request):
#     if request.method == 'POST':
#         form = PhonecheckForm(request.POST)
#         if form.is_valid():
#             phone = form.cleaned_data.get('phone_number')
#             print(phone)  # Check if the phone number is received correctly

#             try:
#                 user = CustomUser.objects.get(phone_number=phone)  # Assuming 'phone_number' is the field name in your CustomUser model
#                 if user:
#                     phone = '+91' + phone
#                     request.session['phone_number'] = phone
#                     print(phone)
#                     # Assuming 'verify' is the method responsible for sending the verification code
#                     verify.send(phone)
#                     return redirect('verify_code')  # Redirect to the verify_code URL
#                 else:
#                     # Handle the case when the user does not exist
#                     # messages.warning(request,'Invalid OTP')
#                     messages.error(request,'Invalid User')
#                     return redirect('otp_login')  # Redirect to the otp_login URL
#             except CustomUser.DoesNotExist:
#                 messages.error(request,'User does not exist')
#                 # messages.warning(request,'Invalid OTP')
#                 return redirect('otp_login')  # Redirect to the otp_login URL
#     else:
#         form = PhonecheckForm()

#     return render(request, 'accounts/otp_login.html', {'form': form})








#Dashboard

@login_required(login_url='signin')
def dashboard(request):
    user = request.user
    addresses = Address.objects.filter()
   
    
    wallet = Wallet.objects.get(user=request.user)
   
    
    
    
        

    if addresses.exists():
        # Select the first address
        address = Address.objects.filter(user=user).first()

    context = { "user" : user,
               "address" : address,
                "wallet": wallet,
            }

    

    return render (request, 'accounts/dashboard.html', context)



def username_password(phone):
    user = CustomUser.objects.filter(phone_number=phone).first()
    return user


def check_phone_number(phone_number):
    try:
        phone_number = CustomUser.objects.filter(phone_number=phone_number).first()
        return True
    except CustomUser.DoesNotExist:
        return False
    

def edit_address(request, id=1):
    address = get_object_or_404(Address, pk=id)
    if request.method == "POST":
        address.name = request.POST['name']
        address.house_name = request.POST['house_name']
        address.address_line_1 = request.POST['address_line_1']
        address.city = request.POST['city']
        address.state = request.POST['state']
        address.country = request.POST['country']
        address.phone = request.POST['phone']
        address.pincode = request.POST['pincode']

        address.save()

        return redirect('dashboard')
    
    context = {'address': address
               
               }

    return render(request, 'accounts/edit-address.html', context)

    

#OTP_COMMENTED

# def forgotPassword(request):
#     if request.method == 'POST':
#         mobile_number_forgotPassword = request.POST.get('phone_number')
#         # Checking for the null case
#         if not mobile_number_forgotPassword:
#             messages.warning(request, 'You must enter a mobile number')
#             return redirect('forgotPassword')

#         # Store the mobile number in the session
#         request.session['mobile_number_forgotPassword'] = mobile_number_forgotPassword

#         user = CustomUser.objects.filter(phone_number=mobile_number_forgotPassword)
#         if user:
#             verify.send('+91' + str(mobile_number_forgotPassword))
#             return redirect('forgotPassword_otp')
#         else:
#             messages.warning(request, 'Mobile number doesnt exist')
#             return redirect('forgotPassword')

#     return render(request, 'accounts/forgotPassword.html')



#OTP_COMMENTED
# def forgotPassword_otp(request):
#     mobile_number_forgotPassword = request.session.get('mobile_number_forgotPassword')

#     if request.method == 'POST':
#         form = VerifyForm(request.POST)
#         if form.is_valid():
#             otp = form.cleaned_data.get('code')
#             if verify.check('+91' + str(mobile_number_forgotPassword), otp):
#                 user = CustomUser.objects.get(phone_number=mobile_number_forgotPassword)
#                 if user:
#                     return redirect('resetPassword')
#             else:
#                 messages.warning(request, 'Invalid OTP')
#                 return redirect('enter_otp')
#     else:
#         form = VerifyForm()

#     return render(request, 'accounts/forgotPassword_otp.html', {'form': form})

# # Similarly, update other views that need to access mobile_number_forgotPassword



def resetPassword(request):
    mobile_number_forgotPassword = request.session.get('mobile_number_forgotPassword')

    if not mobile_number_forgotPassword:
        # Handle the case where mobile_number_forgotPassword is not in the session
        messages.warning(request, 'Mobile number not found. Please start the reset password process again.')
        return redirect('forgotPassword')

    if request.method == 'POST':
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm_password')
        print(password1, password2)
        
        if password1 == password2:
            user = CustomUser.objects.get(phone_number=mobile_number_forgotPassword)
            
            if user is not None:
                print(user)
                user.set_password(password1)
                user.save()
                print('success')

                messages.success(request, 'Password changed successfully')
                return redirect('signin')
        else:
            messages.warning(request, 'Passwords do not match. Please try again')
            return redirect('resetPassword')

    return render(request, 'accounts/resetPassword.html')


#filter
def men(request):
    products = Product.objects.filter(gender="Male")
    return render(request, "store/store.html", {'products':products})

def women(request):
    products = Product.objects.filter(gender="Female")
    return render(request, "store/store.html", {'products':products})



def price_sort(request):
    # Get the price range parameters from the user (e.g., min_price and max_price)
    if request.method == 'POST':
        
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')
        gender = request.POST.get('gender')
        print(max_price)

    #gender checkbox
        if min_price and max_price:
            if gender:
                products = Product.objects.filter(price__gte=min_price, price__lte=max_price, gender=gender)
            else:
                products = Product.objects.filter(price__gte=min_price, price__lte=max_price)
        elif gender:
            products = Product.objects.filter(gender=gender)
        else:
            products = Product.objects.all()



    # Render a partial template with the filtered products
    context = {'products': products}
    return render(request, 'store/store.html', context)








@login_required(login_url='signin')
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'accounts/wishlist.html',context)


def add_to_wishlist(request, id):
    print(id)
    myproduct = get_object_or_404(Product, pk=id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=myproduct)
    response_data = {'created': created}
    return JsonResponse(response_data)


def remove_from_wishlist(request, id):
    myproduct = get_object_or_404(Product, pk=id)
    Wishlist.objects.filter(user=request.user, product=myproduct).delete()
    messages.success(request, 'Product removed from wishlist.')
    return redirect('wishlist')



