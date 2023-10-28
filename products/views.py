from django.shortcuts import render
from django.shortcuts import render, redirect
from.models import *
from django.db.models import Q
from products.models import *



# search products in search bar
def search_product(request):
    product = None
    if request.method == 'POST':
        query = request.POST['query']
        product = Product.objects.filter(Q(product_name__icontains=query)| Q(Category__category_name__icontains=query))
        count = product.count()
    return render(request, "store/search.html", {'products':product,'count':count})

def offer(request):
    cat = Category.objects.all()
    for c in cat:
      offer_cat = CategoryOffer.objects.get(offer_category=c)
      offer_cat.offer_percent



    

    pass
