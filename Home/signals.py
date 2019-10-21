from django.shortcuts import get_object_or_404
# from .models import Order, OrderItem
from paypal.standard.models import ST_PP_COMPLETED
# from paypal.standard.ipn.signals import valid_ipn_received
# from django.dispatch import receiver
 
 
# @receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == ST_PP_COMPLETED:
        # payment was successful
        order = get_object_or_404(Order, user=ipn.custom, ordered = False)
        print(order.id, "this is order is from signals.py")
 
        if order.get_total() == ipn.mc_gross:
            # mark the order as paid
            order.ordered = True
            # order.items.ordered = True
            order.save()