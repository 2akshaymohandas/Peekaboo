from django.contrib import admin
from .views import *

admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Coupon)

