from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.forms import ModelForm
from .models import Item
from phonenumber_field.formfields import PhoneNumberField


from bootstrap_modal_forms.forms import BSModalForm

class SaleAccountForm(BSModalForm):
    class Meta:
        model = Item
        fields = "__all__"


PAYMENT_CHOICES = (
('P','Paypal'),
('M','Mpesa')
)
class CheckoutForm(forms.Form):
    street_address = forms.CharField( widget = forms.TextInput(attrs = {
    'placeholder':"Address 1 for street ","class": "form-control"
    }) )
    apartment_address = forms.CharField(required = False, widget = forms.TextInput(attrs = {
    'placeholder':"Address 2 for Apartment or suite","class": "form-control"
    }))
    country = CountryField(blank_label='(select country)').formfield(widget = CountrySelectWidget(attrs = {
    'class': "custom-select d-block w-100"
    }))
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder':('Enter phone number starting with countrycode i,e +2547xxxx '),"class": "form-control" }), 
            label=("Phone number"), required=True)

    zip_code = forms.CharField(widget = forms.TextInput(attrs = {
        "class": "form-control"
    }))
    same_billing_address = forms.BooleanField(required = False)

    save_info =  forms.BooleanField(required = False)

    payment_option =  forms.ChoiceField( widget = forms.RadioSelect, choices=PAYMENT_CHOICES )
    

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
        