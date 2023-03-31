import json

import requests
from requests.auth import HTTPBasicAuth

MPESA_API_KEY = 'jYwIIGJaGijuawn994Da2CgVchBAeEYQ'
MPESA_API_SECRET = 'xoWKztjJGmnkaR5w'
MPESA_SHORTCODE = '174379'
MPESA_PASSKEY = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

def generate_access_token():
    consumer_key = MPESA_API_KEY
    consumer_secret = MPESA_API_SECRET
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    print("generating token\n\n\n")


    response =json.loads(r.text)
    access_token = response['access_token']
    print(access_token)


    return access_token

generate_access_token()