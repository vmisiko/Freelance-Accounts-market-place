from celery import shared_task
from .models import WithdrawPayouts
from djangoProject.mpesa.b2c import b2c_payments
from . payout import paypal_payout_release
import random
import string

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
            amount = q.amount
            phone = phone_number.split("+")[1]

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
                    "value": q.amount,
                    "currency": "USD"
                },
                "receiver": q.email,
                "note": "congratulations and thank you for working with freelancing Accounts, keep up the spirit.",
                "sender_item_id": sender_batch_id,
            }
            items.append(payout)

        qs.update(status = True)

        paypal_payout_release(items)
