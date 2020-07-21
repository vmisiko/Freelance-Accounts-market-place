import random
import string
import requests
from datetime import datetime
from django.conf import settings
from celery import shared_task
from .models import Logins_passwords, Logins, Unlocks
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


@shared_task
def Unlocks_email(lnm_id,order_id):
    pass

@shared_task
def Logins_email(category,email):
    print(category)
    login = Logins_passwords.objects.get(name= category)

    login_email = login.email
    login_password = login.password

    subject = f"{category} Logins"

    order = {
            "email": login_email,
            "password" :login_password
    }
    html_message = render_to_string('UnlocksApp/email.html', {'order': order})

    plain_message = strip_tags(html_message)
    email_host = settings.EMAIL_HOST_USER

    from_email = email_host
    to = email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

    pass