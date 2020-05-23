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
    amount = models.FloatField(default = 0.0)
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

    