from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from . forms import *
from products.models import *
from django.shortcuts import get_object_or_404
from products.forms import *
from django.forms import inlineformset_factory
from order.models import *
from django.db.models import Q
from django.db.models import Count
import calendar
from datetime import date
from django.db.models.functions import ExtractMonth, ExtractDay, ExtractYear



@login_required(login_url='admin_login')
def admin_panel(request):

    today = date.today()
    
    delivered_orders = Order.objects.filter(status='Delivered')
    
    delivered_orders_by_months = delivered_orders.annotate(
        delivered_month=ExtractMonth('created_at'),
        delivered_day=ExtractDay('created_at')).values('delivered_month', 'delivered_day').annotate(delivered_count=Count('id')).values('delivered_month', 'delivered_day', 'delivered_count')
    
    delivered_orders_month = []
    delivered_orders_number = []
    for d in delivered_orders_by_months:
        month_name = calendar.month_name[d['delivered_month']]
        day_number = d['delivered_day']
        delivered_orders_month.append(f"{month_name} {day_number}")
        delivered_orders_number.append(d['delivered_count'])

    order_by_months = Order.objects.annotate(
        month=ExtractMonth('created_at'),
        day=ExtractDay('created_at')).values('month', 'day').annotate(count=Count('id')).values('month', 'day', 'count')
    
    monthNumber = []
    dayNumber = []
    totalOrders = []
    for o in order_by_months:
        month_name = calendar.month_name[o['month']]
        day_number = o['day']
        monthNumber.append(f"{month_name} {day_number}")
        dayNumber.append(day_number)
        totalOrders.append(o['count'])

    delivered_orders_by_years = delivered_orders.annotate(delivered_year=ExtractYear('created_at')).values('delivered_year').annotate(delivered_count=Count('id')).values('delivered_year', 'delivered_count')
    delivered_orders_year = []
    delivered_orders_year_number = []
    for d in delivered_orders_by_years:
        delivered_orders_year.append(d['delivered_year'])
        delivered_orders_year_number.append(d['delivered_count'])
    
    order_by_years = Order.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(count=Count('id')).values('year', 'count')
    yearNumber = []
    totalOrdersYear = []
    for o in order_by_years:
        yearNumber.append(o['year'])
        totalOrdersYear.append(o['count'])
    
    context ={
        'delivered_orders': delivered_orders,
        'order_by_months': order_by_months,
        'monthNumber': monthNumber,
        'dayNumber': dayNumber,
        'totalOrders': totalOrders,
        'delivered_orders_number': delivered_orders_number,
        'delivered_orders_month': delivered_orders_month,
        'delivered_orders_by_months': delivered_orders_by_months,
        'today': today,
        'order_by_years': order_by_years,
        'yearNumber': yearNumber,
        'totalOrdersYear': totalOrdersYear,
        'delivered_orders_year': delivered_orders_year,
        'delivered_orders_year_number': delivered_orders_year_number,
        'delivered_orders_by_years': delivered_orders_by_years,
    }

    return render(request, 'admin/admin_panel.html', context)




def sales_report(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'admin/sales_report.html', context)




def sales_report_by_product(request, id):
    product = Product.objects.get(pk=id)
    orders = OrderProduct.objects.filter(product=product)
    s = product.product_variant.all()
    total_stock = 0
    for s in s:
      total_stock += s.stock
      
    delivered_orders = []
    delivered_quantity = 0
    for order in orders:
        if order.order.status == 'Delivered':
           delivered_orders.append(order)
           delivered_quantity += order.quantity
    
    number_delivered_orders = len(delivered_orders)

    
    context = {
        'product':product,
        'orders':orders,
        'delivered_quantity':delivered_quantity,
        'number_delivered_orders':number_delivered_orders,
        'total_stock':total_stock,
    }
    return render(request, 'admin/sales_report_by_product.html', context)


    



def sales_date(request):
    if request.method == 'GET':
        form = DateFilterForm(request.GET)
        

        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Query the sales data within the specified date range
            sales_data = Order.objects.filter(created_at__range=[start_date, end_date])

            return render(request, 'admin/sales-report-daily.html', {'sales_data': sales_data, 'form': form,})
    else:
        form = DateFilterForm()

    return render(request, 'admin/sales-report-daily.html', {'form': form})





# admin login page
def admin_login(request):
    if request.user.is_authenticated:
        
        return redirect('admin_panel')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)

       
        user = authenticate(email=email,password=password)
        if user is not None and user.is_superuser:
            print('keri')
            login(request,user)
            return redirect('admin_panel')
        else:
           
            messages.error(request,"User name or password is incorect")
            return redirect('admin_login')
    return render(request,'admin/admin_login.html')



# admin logout 
def admin_logout(request):
    logout(request)
    request.session.flush()
    messages.success(request, "logged out succesfully")
    return redirect('admin_login')


# admin user management
def user(request):
    if request.method=="POST":
        fm = Aforms(request.POST)
        if fm.is_valid():
            fm.save()
            fm = Aforms()
    else:
        fm = Aforms()
    
    stud=CustomUser.objects.all()
    return render(request,'admin/user.html',{'fm':fm,'stud':stud})


# block user 
def block_user(request, id):
    if request.method == "POST":
        user = CustomUser.objects.get(pk=id)
        user.is_active = False
        user.save()
        
        # Check the referer to determine the redirect URL
        referer = request.META.get('HTTP_REFERER')

        if 'search' in referer:
            # Redirect to search page
            
            return redirect('user')
        else:
            # Redirect to user page
            return redirect('user')


# unblock user 
def unblock_user(request, id):
    if request.method == "POST":
        user = CustomUser.objects.get(pk=id)
        user.is_active = True
        user.save()
        # Check the referer to determine the redirect URL
        referer = request.META.get('HTTP_REFERER', '')

        if 'search' in referer:
            # Redirect to search page
            return redirect('search')
        else:
            # Redirect to user page
            return redirect('user')


# admin category management
def category(request):
    pro = Category.objects.all()

   

    context = {
        'pro' : pro,


    }
    return render(request, 'admin/category.html', context)

def category_offer_manage(request,category_name):
    category_obj = Category.objects.get(category_name=category_name)
    category_offer = CategoryOffer.objects.get(offer_category=category_obj)
    products_with_offer = Product.objects.filter(category=category_obj, category__categoryoffer__isnull=False)

    context = {
        
        'products': products_with_offer,
        'category': category_obj,
        'category_offer': category_offer,

    }
    return render(request, 'test.html', context)

#Add category
def add_category(request):
    if request.method == "POST":
        product_form = CategoryForm(request.POST,request.FILES)
        if product_form.is_valid():
            product_form.save()
            return redirect("category")
    else:
        product_form = CategoryForm()
    context = {'product_form': product_form}
    return render(request, 'admin/add_category.html', context)



# edit category
def edit_category(request, id):
    product = get_object_or_404(Category, pk=id)
    if request.method == "POST":
        product_form = CategoryForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('category')
    else:
        product_form = CategoryForm(instance=product)

    context = {
        "product_form": product_form
    }
    return render(request, 'admin/category_edit.html', context)


# delete category
def del_category(request, id):
    if request.method == "POST":
        prod = Category.objects.get(pk=id)
        prod.delete()
        return redirect('category')



# admin brand management

def brand(request):
    pro = Brand.objects.all()
    context = {
        'pro' : pro
    }
    return render(request, 'admin/brand.html', context)

# add new brand
def add_brand(request):
    if request.method == "POST":
        product_form = BrandForm(request.POST,request.FILES)
        if product_form.is_valid():
            product_form.save()
            
            return redirect("brand")
    else:
        product_form = BrandForm()
    context = {'product_form': product_form}
    return render(request, 'admin/add_brand.html', context)

# edit brand

def edit_brand(request, id):
    product = get_object_or_404(Brand, pk=id)
    if request.method == "POST":
        product_form = BrandForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('brand')
    else:
        product_form = BrandForm(instance=product)

    context = {
        "product_form": product_form
    }
    return render(request, 'admin/brand_edit.html', context)

# delete brand

def del_brand(request, id):
    if request.method == "POST":
        prod = Brand.objects.get(pk=id)
        prod.delete()
        return redirect('brand')


# admin products management   
def products(request):
    pro = Product.objects.all()
    context = {
        'pro' : pro
    }
    return render(request, 'admin/products.html', context)


# admin product variant management
def product_variant(request):
    pro = ProductVariant.objects.all()
    context = {
        'pro' : pro
    }
    return render(request, 'admin/product_variant.html', context)



def add_product(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        image_form = ProductImageFormSet(request.POST, request.FILES, instance=Product())
        if product_form.is_valid() and image_form.is_valid():
            myproduct = product_form.save(commit=False)

            #slug generation
            myproduct.slug = slugify(myproduct.product_name)
            myproduct.save()
            image_form.instance = myproduct
            image_form.save()

            return redirect("products")
    else:
        product_form = ProductForm()
        image_form = ProductImageFormSet(instance=Product())
    context = {'product_form': product_form, 'image_form': image_form}
    return render(request, 'admin/add_product.html', context)



# Edit product_details
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('products')
    else:
        product_form = ProductForm(instance=product)

    context = {
        "product_form": product_form
    }
    return render(request, 'admin/product_edit.html', context)


# delete products
def del_product(request, id):
    if request.method == "POST":
        prod = Product.objects.get(pk=id)
        prod.delete()
        return redirect('products')
    

# admin product variant management
def product_variant(request):
    pro = ProductVariant.objects.all()
    context = {
        'pro' : pro
    }
    return render(request, 'admin/product_variant.html', context)


def add_product_variant(request):
    if request.method == "POST":
        product_form = VariantForm(request.POST,request.FILES)
        if product_form.is_valid():
            product_form.save()
            return redirect("product_variant")
    else:
        product_form = VariantForm()
    context = {'product_form': product_form}
    return render(request, 'admin/add_product_variant.html', context)


#Edit product variant 
def edit_product_variant(request, id):
    product = get_object_or_404(ProductVariant, pk=id)
    if request.method == "POST":
        product_form = VariantForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('product_variant')
    else:
        product_form = VariantForm(instance=product)

    context = {
        "product_form": product_form
    }
    return render(request, 'admin/product_variant_edit.html', context)


# Delete product varient
def del_product_variant(request, id):
    if request.method == "POST":
        prod = ProductVariant.objects.get(pk=id)
        prod.delete()
        return redirect('product_variant')



# product size 
def size(request):
    pro = Size.objects.all()
    context = {
        'pro' : pro
    }
    return render(request, 'admin/size.html', context)



def add_size(request):
    if request.method == "POST":
        product_form = SizeForm(request.POST,request.FILES)
        if product_form.is_valid():
            product_form.save()
            
            return redirect("size")
    else:
        product_form = SizeForm()
    context = {'product_form': product_form}
    return render(request, 'admin/add_size.html', context)


#delete size
def del_size(request, id):
    if request.method == "POST":
        prod = Size.objects.get(pk=id)
        prod.delete()
        return redirect('size')
    
@login_required(login_url='admin_login')
def orders(request):
    orders = Order.objects.all().order_by("-created_at")
    return render(request, 'admin/admin_myorder.html', {'orders':orders})

# def search_order(request):
#     order_search = None
#     if request.method == 'POST':
#         query = request.POST['order_query']
#         order_search = Order.objects.filter(Q(user__icontains=query))

#     return render(request, "admin/order-search.html", {'order_search':order_search})
def search_order(request):
    order_search = None
    if request.method == 'POST':
        query = request.POST.get('order_query', '')  # Access the 'order_query' from the POST data
        print(f"Received query: {query}")  # Add a debug statement to print the received query
        order_search = Order.objects.filter(order_number__icontains=query)

    # print(f"Number of results: {order_search.count()}")  # Add a debug statement to print the number of search results

    return render(request, "admin/order-search.html", {'order_search': order_search})


def edit_order(request, id):
    if request.method == "POST":
        status = request.POST.get("status")
        try:
            order = Order.objects.get(pk=id)
            order.status = status
            order.save()
            if status == 'Delivered':
                payment = order.payment
               
                payment.status = 'Success'
                payment.save()


        except Order.DoesNotExist:
            pass
    return redirect("orders")


def order_products(request, id):
    orders = Order.objects.get(pk=id)
    myorder = OrderProduct.objects.filter(order=orders)
    add = orders.address
    context = {
        'orders': orders,
        'myorder':myorder,
        'add': add,
    }
    return render(request, 'admin/admin_orderproducts.html', context) 




def coupon_manage(request):
    coupon = Coupon.objects.all()
    context = {
        "coupon" : coupon,
    }
    return render(request,'admin/coupon.html', context)


def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            print("saved")
            return redirect('coupon_manage')
    else:
        form = CouponForm()

    context = {'form': form}
    return render(request, 'admin/add_coupon.html', context)



def del_coupon(request,id):
    if request.method == "POST":
        coup = Coupon.objects.get(id=id)
        coup.delete()
    return redirect('coupon_manage')



def edit_coupon(request,id):
    if request.method == "POST":
        coup = Coupon.objects.get(id=id)
        form = CouponForm(request.POST, instance=coup)
        if form.is_valid:
            form.save()
        return redirect('coupon_manage')
    else:
        coup = Coupon.objects.get(id=id)
        form = CouponForm(instance=coup)
        context = {
            "form" : form
        }
    return render(request, 'admin/edit_coupon.html', context)



#Product Offer
def product_offer_manage(request):

    offers = Product_offer.objects.all()



    context ={
        'offers': offers
    }


    return render(request,'admin/offer_management.html', context)



def add_offer(request):

    products = Product.objects.all()

    context = {
        'products': products
    }


    if request.method == 'POST':

        product_id = request.POST.get('product')
        discount = request.POST.get('discount')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        product = Product.objects.get(pk=product_id)

        offer = Product_offer(product=product, discount=discount, start_date=start_date, end_date=end_date)
        offer.save()




    return render(request,'admin/add_offer.html', context)


def get_offerprice(request):
    offerprice = request.session.get('offerprice')
    if offerprice is not None:
        
        
        pass
    else:
        # Handle the case where 'offerprice' is not in the session
        pass



def del_pro_offer(request,id):
    if request.method == "POST":
        p_off = Product_offer.objects.get(id=id)
        p_off.delete()
    return redirect('product_offer_manage')









ImageFormSet = ProductImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=5)