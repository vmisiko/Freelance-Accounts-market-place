from django.contrib import admin
from .models import WithdrawPayouts, AccountsModel,Refund, Conversion
from .tasks import mpesa_payout_task,paypal_payout_task

# Register your models here.

class WithdrawPayoutsAdmin(admin.ModelAdmin):
    list_display = ["user", "first_name" ,"phone_number","amount","date","payment_mode","status",]

    actions = ["apply_payout", "mpesa_payout"]

    def apply_payout(self, request, queryset):
        pk_model = []
        for q in queryset:
            pk_model.append(q.pk)
        print(pk_model)
        # mpesa_payout_task.delay(pk_model)
        try:  
            paypal_payout_task.delay(pk_model)
            self.message_user(request, "Please wait this may take a while. Refresh after some few minutes")
        except:
            self.message_user(request, "Failed! Retry again")

    apply_payout.short_description = "Apply Paypal Payout"

    def mpesa_payout(self, request, queryset):
        
        pk_model = []
        for q in queryset:
            pk_model.append(q.pk)
        print(pk_model)
        # mpesa_payout_task.delay(pk_model)
        try:  
            mpesa_payout_task.delay(pk_model)
            self.message_user(request, "Please wait this may take a while. Refresh after some few minutes")
        except:
            self.message_user(request, "Failed! Retry again")
    mpesa_payout.short_description = "Apply Mpesa Payout"

admin.site.register(WithdrawPayouts, WithdrawPayoutsAdmin)

@admin.register(AccountsModel)
class AccountsModelAdmin(admin.ModelAdmin):
    list_display = ["user","phone_number","email","amount", "date"]

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display =["user", "orderid", "amount", "status","date", "mode","seller", "reason"]

@admin.register(Conversion)
class ConversionAdmin(admin.ModelAdmin):
    list_display = ["rate", "date"]