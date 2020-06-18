from django.contrib import admin
from .models import Item , OrderItem,Order, BillingAddress

# admin.site.register(Products)


admin.site.register(BillingAddress)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["created_by",
                    "created_at",
                    "title",
                    "price",
                    "sold",
                 ]
admin.site.register(Item, ItemAdmin)

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
