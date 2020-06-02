from datetime import datetime
from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django_countries.fields import CountryField

from django.template.defaultfilters import slugify
from paypal.standard.ipn.signals import valid_ipn_received
from autoslug import AutoSlugField
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
import time


class Products(models.Model):
    title = models.TextField()
    description = models.TextField()
    price = models.TextField()
    

    def __str__(self):
        return self.title

Category_choices={

("s","Bidding Account"),
("sw", "Take Account"),
("OW", "Transcribing Account")

}

Label_choices={

("P","primary"),
("S", 'secondary'),
("D", "danger")

}

Level_choices = {

    ("Ivy","Ivy"),
    ("Juniour","Junior"),
    ("Intermediate","Intermediate"),
    ("r","Seni0r"),
    
}

class Item(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE,blank = True, null = True, editable = False)
    created_at = models.DateTimeField(auto_now_add= True, blank = True, null = True )
    title = models.CharField(max_length = 100)
    price = models.FloatField(default = 0.0)
    discountprice = models.FloatField(blank= True, null = True)
    category = models.CharField(choices = Category_choices, max_length=2)
    label = models.CharField(choices = Label_choices, max_length=1)
    Level = models.CharField(choices = Level_choices, max_length = 15 ,blank= True, null = True)
    finished_orders = models.IntegerField(default = 1)
    rating = models.IntegerField(default = 50 )
    Reviews =models.IntegerField( default = 1)
    profile = models.CharField( max_length = 20)
    description = models.TextField()
    diplay_pic = models.ImageField(upload_to = "display_pics/%Y%m%d/", max_length =255 )
    contact = models.CharField(max_length=15 ,null = True,blank= True)
    sold = models.BooleanField(default=False)
    # purchased = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Home:product", kwargs ={
            'pk': self.pk
        })
    
    def get_add_to_cart_url(self):

        return reverse("Home:add_to_cart", kwargs ={
            'pk': self.pk
        })

    def get_discount_price(self):
        discount = self.price - self.discountprice
        return discount

    def get_remove_from_cart_url(self):
        return reverse("Home:remove_from_cart", kwargs ={
            'pk': self.pk
        })
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(Item, self).save(*args, **kwargs)

    def get_days(self):
        d1 = timezone.now()
        d2 = self.created_at
        
        dya =  abs(d1-d2).days
        mytuple = (str(dya), "days")
        days = " ".join(mytuple)
        if dya > 0:
            return days
        else:
            seconds = abs(d1-d2).seconds
            houred = round(seconds / 3600)
            
            mytuple = (str(houred), "hours")
            hours = " ".join(mytuple)
            return hours
        
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    quantity = models.IntegerField(default= 1)
    ordered = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.quantity} of {self.item}"
    def after_discount_price(self):
        discounted_price = self.item.price - self.item.discountprice
        return discounted_price

    def get_total_item_price(self):
        price =int(self.quantity) * int(self.item.price)
        print(price, "price of get total item price")
        return price

    def get_total_discount_item_price(self):
        discounted_price = self.item.price - self.item.discountprice

        return self.quantity * discounted_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):

        if self.item.discountprice:

            results= self.get_total_discount_item_price()
            return results
            print(results, "get final price")
        else:
            results = self.get_total_item_price()
            print(results, "get final price")
            return results


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateField(auto_now_add = True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default = False)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE, related_name="user", blank=True, null = True)
    amount = models.IntegerField(default=0.0)
    released = models.BooleanField(default=False)
    refund = models.BooleanField(default=False)
    billing_address = models.ForeignKey(
        "BillingAddress", on_delete = models.SET_NULL, blank = True, null = True)


    def __str__(self):
        return "{}:{}".format(self.id, self.user.username)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()

            # print(total)
            # total += float(od1)
        return total

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    street_address = models.CharField(max_length = 100)
    apartment_address = models.CharField(max_length = 100)
    country = CountryField(multiple = False)
    zip_code = models.CharField(max_length = 100, blank= True, null=True)
    phone_number = PhoneNumberField(max_length=20, blank= True, null=True)
    
    def __str__(self):
        return self.user.username

