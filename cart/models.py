from django.db import models
from accounts.models import CustomUser
from products.models import *

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(Product, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_price(self):
        return sum(item.get_subtotal() for item in self.cart_items.all())
    
    def get_total_products(self):
        return sum(item.quantity for item in self.cart_items.all())
    def __str__(self):
        return str(self.user)


class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_item_product')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def get_subtotal(self):
        return self.product_variant.price * self.quantity
    def __str__(self):
        return str(self.product_variant)     

    

class Coupon(models.Model): 
    coupon_code = models.CharField(max_length = 10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default = 100)
    minimum_amount = models.IntegerField(default=500)


