from django.contrib import admin
from .models import Products,Item, OrderItem,Order, BillingAddress
# Register your models here.

admin.site.register(Products)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(BillingAddress)