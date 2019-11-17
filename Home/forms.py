from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.forms import ModelForm
from .models import Item

PAYMENT_CHOICES = (
('p','Paypal'),
('M','Mpesa')
)
class CheckoutForm(forms.Form):
    street_address = forms.CharField( widget = forms.TextInput(attrs = {
    'placeholder':"Address 1 for street "
    }) )
    apartment_address = forms.CharField(required = False, widget = forms.TextInput(attrs = {
    'placeholder':"Address 2 for Apartment or suite"
    }))
    country = CountryField(blank_label='(select country)').formfield(widget = CountrySelectWidget(attrs = {
    'class': "custom-select d-block w-100"
    }))
    zip = forms.CharField(widget = forms.TextInput(attrs = {
        "class": "form-control"
    }))
    same_billing_address = forms.BooleanField(required = False)
    save_info =  forms.BooleanField(required = False)
    payment_option =  forms.ChoiceField(widget = forms.RadioSelect, choices =PAYMENT_CHOICES )

class Mpesa_checkout(forms.Form):
    
     phone_number = forms.CharField( widget = forms.TextInput(attrs = {
    'placeholder':"2547xxxxxxxxx  "}))
    
class Mpesa_c2b_checkout(forms.Form):

    mpesa_code = forms.CharField( widget = forms.TextInput(attrs = {
    'placeholder':" i.e MNxxxxx "}))

class Sell_item(ModelForm):
    
    class Meta:
        model = Item
        fields = '__all__'
        