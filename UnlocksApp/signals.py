import random
import string
from django.core.mail import send_mail
from MpesaApp.models import LNMOnline2
from django.dispatch import receiver
from django.db.models import signals
from . models import Unlocks, Logins, Logins_passwords
from dashboard.models import Email_notify_admin
from dashboard.tasks import notify_admin
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .tasks import Logins_email

def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits): 
    
    r = ''.join(random.choice(chars) for _ in range(size)) 
    y = "REQ-"+r
    # print(y)
    return y
  
def unique_unlockreq_generator( ): 
    req =random_string_generator(size = 6)
    print(req)
    unlock1 = Unlocks.objects.filter(req_id =req).exists()
    if unlock1:
        req = unique_unlockreq_generator()
        return req
    return req

def unique_loginreq_generator( ): 
    req =random_string_generator(size =6)
    print(req)
    unlock1 = Logins.objects.filter(req_id =req).exists()
    if unlock1:
        req = unique_unlockreq_generator()
        return req
    return req

@receiver(signals.pre_save, sender = Unlocks)
def unlock_pre_signal(sender, instance, *args, **kwargs):
    print("signal landed")
    if not instance.req_id:
        instance.req_id = unique_unlockreq_generator()
    
@receiver(signals.pre_save, sender = Logins)
def login_pre_signal(sender, instance, **kwargs):
    print("signal landed")
    if not instance.req_id:
        instance.req_id = unique_loginreq_generator()

@receiver(signals.post_save, sender=Unlocks)
def unlocks_signal(sender, instance, **kwargs):
    full_Names   = instance.full_Names
    category  = instance.category
    email  = instance.email
    Url  = instance.Url
    status = instance.status

    if status:
        subject = "Unlock Requested"
        message = f"{full_Names}, has requested for {category} Unlock."
        Email_notify_admin.objects.create(
                subject = subject,
                message = message,
            ) 
        notify_admin.delay()
    else:
        pass
    


@receiver(signals.post_save, sender=Logins)
def logins_signal(sender, instance, **kwargs):
    full_Names   = instance.full_Names
    category  = instance.category
    email  = instance.email
    status = instance.status

    if instance.status:

        Logins_email.delay(category, email)
     
    else:

        pass








