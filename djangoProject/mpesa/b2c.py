import requests
from djangoProject.mpesa import keys
from djangoProject.mpesa.access_token2 import generate_access_token_2
from djangoProject.mpesa.utils import formatted_time
from djangoProject.mpesa.encode import generate_password


def b2c_payments(amount, phone_number):
    formated_time = formatted_time()
    amount = amount
    phone_number = phone_number
   

    print(formated_time, " this is formatted time")


    decoded_password = generate_password(formated_time) 
    print(len(decoded_password), " this is decoded password")
    
    my_access_token = generate_access_token_2()
    access_token = my_access_token
    # api_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
    api_url = keys.B2C_URL
    headers = { "Authorization": "Bearer %s" % access_token }
    request = {
        "InitiatorName": "misiko",
        "SecurityCredential":keys.b2c_sec_cred,
        "CommandID": "SalaryPayment",
        "Amount": str(amount),
        "PartyA": keys.b2c_shortcode,
        "PartyB": keys.mssisdn,
        "Remarks": "Thank you for working with us.",
        "QueueTimeOutURL": "https://freelancingaccounts.com/mobile/b2c_callback/",
        "ResultURL": "https://freelancingaccounts.com/mobile/b2c_callback/",
        "Occasion": " widthraw Payout "
    }
    
    response = requests.post(api_url, json = request, headers=headers)
    
    print (response.text)



