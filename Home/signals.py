from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Order, OrderItem
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from dashboard.models import AccountsModel
from notifications.signals import notify
# from django.db.models.signals import post_save
# 
# from myapp.models import MyModel

# def my_handler(sender, instance, created, **kwargs):
#     notify.send(instance, verb='was saved')

# post_save.connect(my_handler, sender=MyModel)
 
 
@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == ST_PP_COMPLETED:
        # payment was successful
        print(ipn.custom)
       
        order = get_object_or_404(Order,user__username=ipn.custom, ordered = False)
        print(order.id, "this is order is from signals.py")
        
        if order.get_total() == ipn.mc_gross:
            # mark the order as paid
            order.ordered = True
            order.items.ordered = True
            order.amount= int(ipn.mc_gross)
            # order.items.ordered = True
            order.save()
        qr = AccountsModel.objects.filter(user__username=ipn.custom).exists()
        
        if qr:
            qs = AccountsModel.objects.get(user__username=ipn.custom)
            amount1 = int(qs.amount)
            amount = amount1 + int(ipn.mc_gross)
            qs.amount= amount
            qs.phone_number = ipn.contact_phone
            qs.email = ipn.payer_email
            qs.save()
            print("accounts model updated")
            notify.send(user =ipn.custom,recipient=ipn.custom, verb=f'Your payment of  ${ipn.mc_gross} was recieved suceesfuly')

        else:
            q = User.objects.get(username=ipn.custom)
            account= AccountsModel.objects.create(
                user_id=q.id ,
                amount= ipn.mc_gross,
                phone_number = ipn.contact_phone,
                email = ipn.payer_email
            )
            account.save()
            print("accounts model saved")
            