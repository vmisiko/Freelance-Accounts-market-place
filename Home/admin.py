from django.contrib import admin
from .models import Products,Item, OrderItem,Order, BillingAddress, LNMOnline
# Register your models here.

admin.site.register(Products)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(BillingAddress)


class LNMOnlineAdmin(admin.ModelAdmin):
    list_display = ["Amount",
                    "MpesaReceiptNumber",
                    "TranscationDate",
                    "PhoneNumber",
                    "paid"
                 ]

admin.site.register(LNMOnline,LNMOnlineAdmin)