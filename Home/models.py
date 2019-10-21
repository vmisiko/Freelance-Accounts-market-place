from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from django_countries.fields import CountryField
from paypal.standard.ipn.signals import valid_ipn_received


# Create your models here.
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

class Item(models.Model):
    title = models.CharField(max_length = 100)
    price = models.FloatField()
    discountprice = models.FloatField(blank= True, null = True)
    category = models.CharField(choices = Category_choices, max_length=2)
    label = models.CharField(choices = Label_choices, max_length=1)
    slug = models.SlugField()
    description = models.TextField()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Home:product", kwargs ={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("Home:add_to_cart", kwargs ={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("Home:remove_from_cart", kwargs ={
            'slug': self.slug
        })



class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    quantity = models.IntegerField(default= 1)
    ordered = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.quantity} of {self.item}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discountprice
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discountprice:
            return self.get_total_discount_item_price()
        return self.get_total_item_price

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateField(auto_now_add = True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default = False)
    billing_address = models.ForeignKey(
        "BillingAddress", on_delete = models.SET_NULL, blank = True, null = True)


    def __str__(self):
        return "{}:{}".format(self.id, self.user.username)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    street_address = models.CharField(max_length = 100)
    apartment_address = models.CharField(max_length = 100)
    country = CountryField(multiple = False)
    zip_code = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.user.username
from .signals import payment_notification

valid_ipn_received.connect(payment_notification)