from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Order, OrderItem, Item
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from dashboard.models import AccountsModel
from notifications.signals import notify
from django.db.models.signals import pre_save

import random
import string 
from django.utils.text import slugify 
  
def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits): 
    return ''.join(random.choice(chars) for _ in range(size)) 
  
def unique_slug_generator(instance, new_slug = None): 
    if new_slug is not None: 
        slug = new_slug 
    else: 
        slug = slugify(instance.title) 
    Klass = instance.__class__ 
    qs_exists = Item.objects.filter(slug = slug).exists() 
      
    if qs_exists: 
        new_slug = "{slug}-{randstr}".format( 
            slug = slug, randstr = random_string_generator(size = 4)) 
              
        return unique_slug_generator(instance, new_slug = new_slug) 
    return slug 

@receiver(pre_save, sender =Item)
def pre_save_item_receiver(sender, instance, *args, **kwargs): 
   if not instance.slug: 
       instance.slug = unique_slug_generator(instance) 
       
  
@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == ST_PP_COMPLETED:
        # payment was successful
        print(ipn.custom)
       
        order = get_object_or_404(Order,user__username=ipn.custom, ordered = False)
        print(order.id, "this is order is from signals.py")
        net_amount = float(ipn.mc_gross) - float(ipn.mc_fee)

        if order.get_total() == ipn.mc_gross:
            # mark the order as paid
            

            order.ordered = True
            order.items.ordered = True
            order.amount= float(net_amount)
            # order.items.ordered = True
            order.save()
        qr = AccountsModel.objects.filter(user__username=ipn.custom).exists()
        
        if qr:
            qs = AccountsModel.objects.get(user__username=ipn.custom)
            amount1 = float(qs.amount)
            amount = amount1 + float(ipn.mc_gross)
            qs.amount= net_amount
            qs.phone_number = ipn.contact_phone
            qs.email = ipn.payer_email
            qs.save()
            print("accounts model updated")
            # notify.send(user =ipn.custom,recipient=ipn.custom, verb=f'Your payment of  ${ipn.mc_gross} was recieved suceesfuly')

        else:

            q = User.objects.get(username=ipn.custom)
            account= AccountsModel.objects.create(
                user_id=q.id ,
                amount= net_amount,
                phone_number = ipn.contact_phone,
                email = ipn.payer_email

            )
            account.save()
            print("accounts model saved")
            