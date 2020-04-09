import requests
from djangoProject.mpesa import keys
from djangoProject.mpesa.access_token import generate_access_token
from djangoProject.mpesa.utils import formatted_time
from djangoProject.mpesa.encode import generate_password

def b2c_payments(amount, phone_number):
    formated_time = formatted_time()
    amount = amount
    phone_number = phone_number
    # print(amount, phone_number, "this are the cridentials")

    print(formated_time, " this is formatted time")


    decoded_password = generate_password(formated_time) 
    print(len(decoded_password), " this is decoded password")
    my_access_token = generate_access_token()
    access_token = my_access_token
 
    api_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
    headers = { "Authorization": "Bearer %s" % access_token }
    request = {
        "InitiatorName": keys.InitiatorName,
        "SecurityCredential":"p9LEWlRYM8g+/zJHjyQ3Hwfv77Re7I8xLskDKI/RefvKGSC/KdlbMt/gPFmIqTB6gjNnav8IBWqekTfh/5a0cuFQmvnz/jp3z0ZytRcaI+gBmF+JWd2iiIo6UFW4Ve7SnSFtyY3vkdjo5TVNnv1u1oJgyN7lGMMdAjeaqBdISwOQ4e9UJq3fA4nzQUf2+kPYNQpIi4Me3sJ8MGNnJDjgPNmnCm1Io6YF2hqmErhSE95SCMaIVXGJgegoH+WGF8oRO2PxxeIpfumcTNG8fs7dSfYu8eNV+NUCOoXB6DyPnx9rtUG9duI2nPG03rtrI1frtYpkdxtVxvIpyqllbp0HfA==",
        "CommandID": "SalaryPayment",
        "Amount": str(amount),
        "PartyA": keys.short_code,
        "PartyB": keys.mssisdn,
        "Remarks": "Congratulations for working in Divine ventures, keep it up.",
        "QueueTimeOutURL": "https://e919cddc.ngrok.io/mobile/b2c_callback/",
        "ResultURL": "https://e919cddc.ngrok.io/mobile/b2c_callback/",
        "Occasion": "Krismas"
    }
    
    response = requests.post(api_url, json = request, headers=headers)
    
    
    print (response.text)


