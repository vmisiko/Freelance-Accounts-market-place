from django.contrib import admin
from .models import Item , OrderItem,Order, BillingAddress

# admin.site.register(Products)
admin.site.register(Item)

admin.site.register(BillingAddress)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["user",
                    "item",
                    "quantity",
                    "ordered"
                 ]

admin.site.register(OrderItem,OrderItemAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ["user",
                    "ordered_date",
                    "ordered",
                    "seller",
                    "amount",
                    "released",
                    "refund",
                 ]

admin.site.register(Order,OrderAdmin)
