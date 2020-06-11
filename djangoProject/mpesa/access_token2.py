import requests
from requests.auth import HTTPBasicAuth
from djangoProject.mpesa import keys


def generate_access_token_2():

    consumer_key = keys.b2c_consumer_key
    consumer_secret = keys.b2c_consumer_secret
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    # api_URL = keys.access_token_api_url
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret)) 
    

    json_request = r.json()
    print(json_request)
    my_access_token = json_request["access_token"]

    print(my_access_token)
    return my_access_token

generate_access_token_2()