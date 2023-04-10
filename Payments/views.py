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



    template_name = "Users/card.html"

    def get_context_data(self,*args,**kwargs):

        context = super(PaymentView, self).get_context_data(**kwargs)

        # currencies = stripe.CountrySpec.list()['data'][0][  "supported_payment_currencies"]
        currencies=['KES','TZS','USD','JPY']
        context['countries']=currencies
        print(currencies)
        return context

    def post(self, request, *args, **kwargs):
        # Get the user's card information from the form
        if request.method=="POST":
            card_number = request.POST.get("card")
            exp_month = request.POST.get("month")
            exp_year = request.POST.get("year")
            cvc = request.POST.get("cvc")
            names=request.POST.get('names')
            currency=request.POST.get('currency')
            amount=request.POST.get('amount')
            message=request.POST.get('message')

            print(card_number,currency,amount)
            token=stripe.Token.create(
                  card={
                    'number': card_number,
                    'exp_month': exp_month,
                    'exp_year': exp_year,
                    'cvc': cvc,
                      "name":names,

                  },

                )
            customer = stripe.Customer.create(
                source=token,email= request.user,name=names
            )
            # print(customer)

            # # Create a Stripe Charge object to process the payment
            amount=int(amount)*100
            currency=currency.lower()
            charge = stripe.Charge.create(
                amount=amount,
                currency=currency,
                customer=customer.id,
                description="Test payment",
                metadata={
                    'project_id':request.session['project-id'],
                    'message':message,
                    'user':request.user
                }
            )

            # # Render a confirmation page if the payment was successful
            return self.render_to_response({"success": True})







@csrf_exempt
def StripeWebhookView(request):
    # @csrf_protect

    if request.method=="POST":
        payload = request.body
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        endpoint_secret = "whsec_WLix6iladiKi5cALUPKuaPolsf8JKH1H"

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)

        if event['type'] == 'charge.failed':
            charge = event['data']['object']
            print(charge)
        elif event['type'] == 'charge.pending':
            charge = event['data']['object']
            print(charge)
        elif event['type'] == 'charge.succeeded':
            charge = event['data']['object']
            print(charge['metadata'])
            amount=charge['amount']
            project_id=charge['metadata']['project_id']
            message=charge['metadata']['message']
            transact_id=charge['id']
            brand=charge['payment_method_details']['card']['brand']
            currency=charge['currency']
            country=charge['payment_method_details']['card']['country']
            name=charge['billing_details']['name']
            created=charge['created']
            user=charge['metadata']['user']
            print(type(amount))
            print("\n\n\n\n\n\n\n")
            user=MyUser.objects.get(email=user)
            payment = StripeCardPayments.objects.create(
                user=user,
                amount=amount,
                project_id=project_id,
                transact_id=transact_id,
                message=message,
                currency=currency,
                name=name,
                country=country,
                brand=brand,
                created=created
            )
            payment.save()
            obj = Project.objects.get(id=project_id)
            obj.achieved_amount+=amount/100
            obj.save()

            secret_key='sk_test_51MrhGPHSDxMMHnYTxwz5LLK9vGRHde981TLoCjmE9HNOmtbvAlIZbn9eCk29JFq98zziGrwKOxfj1ol5N9TDEOHo00eHUdjtjw'
            # ... handle other event types
        else:
            print('Unhandled event type {}'.format(event['type']))
        return HttpResponse(status=200)





class PaymentSuccess(TemplateView):
    template_name = 'Payments/success.html'
class PaymentError(TemplateView):
    template_name = 'Payments/failed.html'