import requests
from requests.auth import HTTPBasicAuth
from djangoProject.mpesa import keys

def generate_access_token():
    print('acces token called')
    consumer_key = keys.consumer_key
    consumer_secret = keys.consumer_secret

    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    # api_URL = keys.access_token_api_url
    # print(api_url, "access token cllaed")
    
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret)) 
    # print (r.json())

    json_request = r.json()
    my_access_token = json_request["access_token"]
    print(my_access_token, " this is my access token")

    return my_access_token