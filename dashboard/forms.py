from django import forms
from django.forms import ModelForm
from .models import WithdrawPayouts


class PayoutForm(ModelForm):
    class Meta:
        model = WithdrawPayouts
        exclude = ["user","date","status"]

        
