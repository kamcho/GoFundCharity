import base64
import json
from base64 import b64encode
from datetime import datetime
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.urls import reverse

import requests
from django.http import HttpResponse
from requests.auth import HTTPBasicAuth

from GoFundKE.settings import MPESA_SHORTCODE, MPESA_PASSKEY, MPESA_API_SECRET, MPESA_API_KEY
from Payments.models import MpesaPayment

def generate_access_token():
    consumer_key = MPESA_API_KEY
    consumer_secret = MPESA_API_SECRET
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    print("generating token\n\n\n")


    response =r.json()
    access_token = response['access_token']
    print(access_token)

    return redirect('deposit')


class Stripe(TemplateView):
    template_name = 'Payments/Stripe.html'

class Mpesa(TemplateView):
    template_name = 'Payments/Mpesa.html'

    def post(self,request,*args,**kwargs):
        if request.method=="POST":
            amount=request.POST.get('amount')
            print("Slave",amount)
            phone_number = '254742134431'  # replace with the customer's phone number
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            passwords = MPESA_SHORTCODE+MPESA_PASSKEY+timestamp
            print(passwords)
            encoded=base64.b64encode(passwords.encode())
            password=encoded.decode('utf-8')
            consumer_key = MPESA_API_KEY
            consumer_secret = MPESA_API_SECRET
            api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

            r = requests.get(api_URL, auth=HTTPBasicAuth(MPESA_API_KEY, MPESA_API_SECRET))
            print("generating token\n\n\n")

            response = json.loads(r.text)
            access_token = response['access_token']
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            data = {
                'BusinessShortCode': MPESA_SHORTCODE,
                'Password': password,
                'Timestamp': timestamp,
                'TransactionType': 'CustomerPayBillOnline',
                'Amount': amount,
                'PartyA': phone_number,
                'PartyB': MPESA_SHORTCODE,
                'PhoneNumber': phone_number,
                'CallBackURL': 'https://cd64-197-156-137-164.eu.ngrok.io/payments/',
                'AccountReference': 'Test',
                'TransactionDesc': 'Test',
            }
            response = requests.post('https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', json=data,
                                     headers=headers)
     
        return HttpResponse(response)
@csrf_exempt
def confirmation(request):
    print("USER ACCEPTED \n\n")


    return HttpResponse("body")


class PaymentSuccess(TemplateView):
    template_name = 'Payments/success.html'
class PaymentError(TemplateView):
    template_name = 'Payments/failed.html'