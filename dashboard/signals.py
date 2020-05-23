from django.shortcuts import get_object_or_404
from .models import AccountsModel
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.db.models import signals
from MpesaApp.models import LNMOnline
from .models import AccountsModel, Conversion
from allauth.account.signals import user_signed_up
from .models import AccountsModel
from Home.models import Order
# from paypal.standard.ipn.signals import valid_ipn_received

@receiver(user_signed_up)
def save_Account(sender, **kwargs):
    request = kwargs['request'] 
    user = kwargs['user']
    print(user, request)
    
    account = AccountsModel.objects.create(
        user = user
    )
    





@receiver(signals.post_save, sender = LNMOnline)
def send_lnm_signal(sender, instance, **kwargs):

    phone_number = instance.PhoneNumber
    amount0 = instance.Amount
    conversion = Conversion.objects.all()
    rate = [con.rate for con in conversion][0]
    print(rate, "Mpesa rate in signals working")
    amount1 = int(amount0)/int(rate)
    print(amount1, "rate in dollars")

    if AccountsModel.objects.filter(phone_number= phone_number).exists():
        account = AccountsModel.objects.get(phone_number= phone_number)
        user = account.user
        amount2 = account.amount
        amount = int(amount1) + int(amount2)
        account.amount = amount
        account.save()
        print("updated Accounts")

        order = Order.objects.get(user__username = user, ordered=False)
        order.amount = int(amount1)
        order.save()

    else:
        print("Account with that phone number does not exist")











        
    