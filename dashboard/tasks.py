import random
import string
import requests
import datetime
from django.conf import settings
from celery import shared_task
from .models import WithdrawPayouts, Conversion, AccountsModel, Email_notifications, Email_notify_admin
from Home.models import Order,Item
from djangoProject.mpesa.b2c import b2c_payments
from . payout import paypal_payout_release
from django.utils import timezone
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from MpesaApp.models import LNMOnline
from django.contrib.auth.models import User
from django.core.mail import send_mail


sender_batch_id =''.join(
    random.choice(string.ascii_uppercase) for i in range(12)
        
    )

@shared_task
def mpesa_payout_task(pk_model):

    queryset = WithdrawPayouts.objects.filter(pk__in = pk_model)
    print("Celery worker now working")
    if queryset:
        print("qs available")
        qs = queryset.filter(status=False, payment_mode="M")
        
        for q in qs:
            phone_number = str(q.phone_number)
            amount1 = q.amount_dispensed
            phone = phone_number.split("+")[1]

            # convert to kES
            conversion = Conversion.objects.all()
            rate1 = [con.rate for con in conversion][0]
            rate = float(rate) - 2 
            amount = float(amount1)*float(rate)

            print(phone)
            # b2c_payments(amount,phone)
            try:
                b2c_payments(amount,phone)
                q.status= True
                q.save()
            except:
                pass

    else:
        print("qs not available")
        
@shared_task
def paypal_payout_task(pk_model):

    queryset = WithdrawPayouts.objects.filter(pk__in = pk_model)
    print("Celery worker now working")
    if queryset:

        qs = queryset.filter(status=False, payment_mode="p")
        

        items = [ ]
       
        for q in qs:       
            payout = {
                "recipient_type": "EMAIL",
                "amount": {
                    "value": q.amount_dispensed,
                    "currency": "USD"
                },
                "receiver": q.email,
                "note": "Congratulations and thank you for working with freelancing Accounts, keep up the spirit.",
                "sender_item_id": sender_batch_id,
            }
            items.append(payout)

        qs.update(status = True)

        paypal_payout_release(items)


@shared_task
def release_payment():
    # accounts = AccountsModel.objects.all()
    orders = Order.objects.filter(ordered=True, released=False, refund= False)
    d1 = timezone.now()
    for order in orders:
        print("worker order releasing")
        d2 =order.ordered_date

        amount = order.get_total()

        buyer = order.user


        seller = order.seller

        print(f" buyer and seller: {buyer} - {seller}")

        account_buyer = AccountsModel.objects.get(user__username= buyer)
        

        if abs(d1-d2).days >=3:
            amount1 = int(account_buyer.amount) - int(amount)

            order.released = True
            for org in order.items.all():
                item_id = org.item.id

                item = Item.objects.get(id=item_id )
                item.sold = True
                item.save()

            order.save()
            print(F'{amount1}, is the buyers balance from {account_buyer.amount}')
            account_buyer.amount = int(amount1)

            account_buyer.save()
            
            seller_account = AccountsModel.objects.get(user__username = seller)
            amount2 = seller_account.amount
            amount_deduct = int(amount) - 2
            print(amount, amount_deduct, "this is deducted amounts")
            amount3 = int(amount2) + int(amount_deduct)

            seller_account.amount = amount3

            seller_account.save()
            
        else:

            print(" three days still not yet completed")

@shared_task
def exchange_rate():
    api_url ="https://www.freeforexapi.com/api/live?pairs=USDKES"
    r =requests.get(api_url)
    json_data =r.json()
    rate1 = json_data["rates"]["USDKES"]["rate"]
    print(round(rate1), "this is exchange rate api")
    rate = round(rate1)

    conversion = Conversion.objects.all()
    for con in conversion:
        con.rate = int(rate)
        con.date = datetime.now()
        con.save()


@shared_task()
def send_email_notifications():

    email_notif = Email_notifications.objects.filter(status= False)
    email_host = settings.EMAIL_HOST_USER
    for em in email_notif:

        subject = em.title 
        order = {
            "title": em.title,
            "text" : em.message
        }
        html_message = render_to_string('dashboard/email.html', {'order': order})

        plain_message = strip_tags(html_message)

        from_email = email_host
        to = em.seller_email

        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        em.status = True
        em.save()

       

@shared_task
def lnm_validation_save(lnm_id,order_id):

    instance_id = lnm_id
    order_id = order_id 

    lnm = LNMOnline.objects.get(id = instance_id )
    lnm.paid = True
    lnm.save()

    order = Order.objects.get(id=order_id)       
    order.ordered = True
    order.items.ordered = True
    order.save()
    

    items = order.items.all()
    for i in items:
        item_id = i.item.id

        print(item_id, "lnm item id")
        item = Item.objects.get(id = item_id)
        print(item)
        item.sold = True
        item.save()
        print("item saved")
   
    
    print("lnm and order saved")
        
@shared_task
def refund_order_save(order_id):
    orderid = order_id
    order =  Order.objects.get(id=orderid)
    order.refund= True
    order.save()

    items = order.items.all()
    for i in items:
        item_id = i.item.id

        print(item_id, "lnm item id")
        item = Item.objects.get(id = item_id)
        
        item.sold = False
        item.save()
        print("item saved")


@shared_task
def notify_admin():

    notifications = Email_notify_admin.objects.filter(status=False)

    for notif in notifications:

        subject = notif.subject
        message = notif.message

        to ="victormisiko.vm@gmail.com"
        email_host = settings.EMAIL_HOST_USER

        send_mail(subject, message, email_host, [to])

        notif.status = True
        notif.save()

@shared_task
def order_save_notifications(ord_notif):

    ord_notif = ord_notif
    if "seller" in ord_notif:
        seller = ord_notif["seller"]
        buyer = ord_notif["buyer"]
        s= User.objects.get(username=seller)
        b = User.objects.get(username=seller)
        seller_email = s.email
        buyer_email = b.email
        ordered = ord_notif["ordered"]

        released = ord_notif["released"]
        refund = ord_notif["refund"]
        order1 ={}
        order2 = {}
        email_host = settings.EMAIL_HOST_USER
            
        if ordered ==True and released==False and refund == False:

            order1 = {

                "title" : "Your Item has been Ordered!!",
                "text" : f"Your product has been ordered by buyer {buyer}.Kindly visit your account to check for your orders and transactions "
            }

            order2 = {
                
            "title" : "You have Ordered!!",
            "text" : f"Your have Ordered a product from Seller {seller}.Kindly visit your account to check for your orders and transactions "
        }

        elif ordered ==True and released==True and refund == False:
            order1 = {

                "title" : "Your cash has been Released!!",
                "text" :  f"Your cash has been released by buyer {buyer}.Kindly visit your account to check your account balance, orders and transactions "
            }

            order2 = {
            
                "title" : "Amount released!!",
                "text" : f"Your cash has been released to seller {seller}. Kindly visit your account to check your account balance,orders and transactions"
            }

        elif ordered==True and released==False and refund == True:

            order1 = {
                    
                "title" : "Order cancelled!!",
                "text" :  f"The order to your product has been cancelled by {buyer}.Kindly visit your account and email us immidiately if you have complains pertaining this action."
            }

            order2 = {
                    
                "title" : "Order cancelled!!",
                "text" : f"Your have cancelled your order to by from {seller}. Kindly visit your account to check your account balance,orders and transactions"
            }

        elif ordered==False and released==False and refund == False:

            order1 = {
                    
                "title" : "Order in Progress!!",
                "text" :  f"The order to your product is in progress by {buyer}."
            }

            order2 = {
                    
                "title" : "Order In Progress",
                "text" : f"Your have initiated an order from {seller}. Kindly select the payment option of your choice and complite your order"
            }
            

        else:
            order1.clear()
            order2.clear()


        print(order1)
        print(order2)

        email_notif1 = Email_notifications.objects.create(
            seller = seller,
            buyer = buyer,
            title = order1["title"],
            message= order1["text"],
            seller_email = seller_email,
            buyer_email = buyer_email

        )

        email_notif1.save()

        email_notif2 = Email_notifications.objects.create(
            
            seller = seller,
            buyer = buyer,
            title = order2["title"],
            message= order2["text"],
            seller_email = seller_email,
            buyer_email = buyer_email,

        )
        
        email_notif2.save()

        try:

            send_email_notifications.delay()

        except:

            pass

      
