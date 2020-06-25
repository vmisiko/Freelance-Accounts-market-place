from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from Home.models import Order
# Create your models here.

mode_choices = {
    ("M","Mpesa"),
    ("p","Paypal")
}

class WithdrawPayouts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    first_name= models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    phone_number = PhoneNumberField(max_length = 15)
    email = models.CharField(max_length = 50)
    amount_requested = models.FloatField(default = 0.0)
    amount_dispensed = models.FloatField(default = 0.0)
    date = models.DateTimeField(auto_now_add = True,blank = True, null= True)
    payment_mode = models.CharField(choices= mode_choices,max_length = 20,)
    status = models.BooleanField(default= False)
    
    class Meta:
        get_latest_by = ['-date']


class AccountsModel(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    amount = models.FloatField(default= 0.0)
    date = models.DateTimeField(auto_now_add=True)

    

class Refund(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    orderid = models.IntegerField(default=0.0)
    amount = models.FloatField(default = 0.0)
    seller = models.CharField(max_length= 500,null=True, blank = True  )
    item = models.CharField(max_length= 500,null=True, blank = True)
    status = models.BooleanField(default = False)
    date = models.DateTimeField(auto_now_add=True,null=True, blank = True )
    reason = models.CharField( max_length = 200, null= True, blank=True)
    mode = models.CharField(max_length=20, null=True, blank = True)

class Conversion(models.Model):
    rate =  models.FloatField(default = 0.0)
    date = models.DateTimeField(auto_now_add=True,null=True, blank = True )


class Paypal_callbacktb(models.Model):
    resultid = models.CharField(max_length = 50,blank = True,null = True)
    payout_batch_id  = models.CharField(max_length = 20,blank = True,null = True)
    batch_status = models.CharField(max_length = 20,blank = True,null = True)
    time_created = models.DateTimeField(blank = True,null = True)
    time_completed = models.DateTimeField(blank = True,null = True)
    sender_batch_id = models.CharField(max_length = 20,blank = True,null = True)
    amount = models.FloatField(default = 0.0)
    currency = models.CharField(max_length = 20,blank = True,null = True)
    fees = models.FloatField(default = 0.0)
    payments = models.IntegerField(default = 0)

class Email_notifications(models.Model):
    seller = models.CharField(max_length=50, null=True, blank=True)
    buyer =  models.CharField(max_length=50, null=True, blank=True)
    title =  models.CharField(max_length=200, null=True, blank=True)
    message =  models.CharField(max_length=500, null=True, blank=True)
    seller_email = models.EmailField(max_length=100,null=True, blank=True)
    buyer_email = models.EmailField(max_length=100,null=True, blank=True)
    status =models.BooleanField(default=False)
    date =models.DateTimeField(auto_now_add=True)