import base64
import requests
from math import ceil
from djangoProject.mpesa import keys
from datetime import datetime
from djangoProject.mpesa.access_token import generate_access_token
from djangoProject.mpesa.encode import generate_password
from djangoProject.mpesa.utils import formatted_time


# print(datetime.now())2019-10-23 19:35:31.462259
# 2019-10-23 19:35:31.462259 = 





def lipa_na_mpesa(phone_number, amount , callbackurl, AccountReference,):
    print("lnm, called")
    phone = phone_number
    account = AccountReference  
    callbackurl = callbackurl
    formated_time = formatted_time()
    amount= ceil(float(amount))

    print(formated_time, " this is formatted time")

    decoded_password = generate_password(formated_time) 
    # print(decoded_password, " this is decoded password")
    

    my_access_token = generate_access_token()
    print(my_access_token, " this is my access token")

    
    access_token = my_access_token
    # api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    api_url = keys.lnm_api_url

    headers = { "Authorization": "Bearer %s" % access_token }

    request = {
        "BusinessShortCode": keys.bussiness_shortcode,
        "Password": decoded_password,
        "Timestamp": formated_time,
        "TransactionType": "CustomerBuyGoodsOnline",
        "Amount": str(amount),
        "PartyA": phone,
        "PartyB": keys.till,
        "PhoneNumber": phone,
        "CallBackURL": callbackurl,
        "AccountReference": account,
        "TransactionDesc": "Buy Freelancing account Account",
      }
      
    response = requests.post(api_url, json = request, headers=headers)
      
    print (response.text)

    return response.text

