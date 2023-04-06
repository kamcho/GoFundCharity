from .models import *
from django.shortcuts import redirect, render
from django.views.generic import ListView,TemplateView,DetailView
from Users.forms import MyUserCreationForm
from django.contrib.auth import authenticate
from django.contrib import messages
import stripe
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


# Create your views here.

def register(request):
    if request.method=="POST":
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # username=form.cleaned_data.get('email')
            # print(username)
            # messages.success(request,f"Account for {username} is succsesfully created. Login")
            return redirect('login')
        else:
            print("failed")
    else:
        print("failed")
        form=MyUserCreationForm
    return render (request,'Users/register.html', {'form':form})


class Profiles(ListView):
    model=Profile
    template_name = 'Users/profile.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Profiles, self).get_context_data(**kwargs)
        user = self.request.user
        print(type(user))
        context['projects'] = Project.objects.filter(user=user)
        print(context)
        return context

    def post(self, request, *args, **kwargs):
        profile=Profile.objects.get(user=self.request.user)
        fname = request.POST.get('first-name')
        new_phone_number = request.POST.get('phone_number')
        lname = request.POST.get('last-name')
        country = request.POST.get('country')
        city = request.POST.get('city')
        area = request.POST.get('area')

        # Check if the password is correct
        profile.phone = new_phone_number
        profile.first_name=fname
        profile.last_name=lname
        profile.country=country
        profile.city=city
        profile.area=area
        profile.save()

        messages.success(request, 'Phone number updated successfully')
        return redirect('profile')

class Home(TemplateView):
    template_name = 'Users/trade.html'
    
    def get_context_data(self,*args,**kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['charities']=Project.objects.all()
        return context

class ProjectDetail(DetailView):
    template_name='Users/projectid.html'
    context_object_name='project'
    model=Project

    def post(self,request,*args,**kwargs):
        if request.method=="POST":
            choice=request.POST.get('line')
            print(choice)
            request.session['project-id']=self.kwargs['pk']
            print(request.session['project-id'])

            if choice=='Card':
                return redirect('https://donate.stripe.com/test_bIY4j94kGcw31QQ000')
            else:
                return redirect('deposit')


import stripe
from django.http import HttpResponse
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
            print(charge)
            # ... handle other event types
        else:
            print('Unhandled event type {}'.format(event['type']))
        return HttpResponse(status=200)


class QandA(TemplateView):
    template_name = 'Users/QandA.html'

    def get_context_data(self, *args, **kwargs):
        context = super(QandA, self).get_context_data(**kwargs)
        context['quizes'] = Quizes.objects.all()
        return context
    def post(self,request):
        if request.method=="POST":
            quiz=request.POST.get('quiz')
            quiz_obj=Quizes.objects.create(user=request.user)
            quiz_obj.quiz=quiz
            quiz_obj.save()

            return redirect('quizes')
        

class Contacts(TemplateView):
    template_name='Users/contacts.html'

    def post(self, request):
        if request.method == "POST":
            quiz = request.POST.get('quiz')
            names=request.POST.get('names')
            location=request.POST.get('location')
            phone=request.POST.get('phone')
            mail=request.POST.get('mail')
            
            mail_obj = Mails.objects.create()
            mail_obj.quiz = quiz
            mail_obj.mail=mail
            mail_obj.location=location
            mail_obj.phone=phone
            mail_obj.names=names
            mail_obj.save()

            return redirect('quizes')
    

class StartCharity(TemplateView):
    template_name = 'Users/startcharity.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StartCharity, self).get_context_data(**kwargs)
        try:
            context['data1']=self.request.session['data1']
            context['data2']=self.request.session['data2']
        except:
            pass
        return context

    def post(self, request, *args, **kwargs):
        print("ENTERD POST")
        if "form1" in request.POST:
            data={
            "title" :request.POST.get('title'),

            "fname" : request.POST.get('first-name'),
            "lname" : request.POST.get('last-name'),

            "country" : request.POST.get('country'),
            "city" : request.POST.get('city'),
            "area" : request.POST.get('street')
            }
            request.session['data1']=data

            print(data)
            return redirect('gofund')
        if "form2" in request.POST:
            print("FORM2 ONLINE \n\n\n")
            form2_data={
            "beneficiary" : request.POST.get('beneficiary'),
            "problem" : request.POST.get('problem'),
            "solution" : request.POST.get('solution'),
            "target" : request.POST.get('target'),
            "expiry" : request.POST.get('expiry')
            }
            # print(data)

            request.session['data2']=form2_data


            return redirect('confirmproject')


class ConfirmProject(TemplateView):
    template_name = 'Users/confirm_details.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ConfirmProject, self).get_context_data(**kwargs)
        context['data1']=self.request.session['data1']
        context['data2']=self.request.session['data2']
        return context

    def post(self,request,*args,**kwargs):
        if request.method=='POST':
            project = Project.objects.create(user=self.request.user)
            project.title = request.session['data1']['title']
            project.first_name = request.session['data1']['fname']
            project.last_name = request.session['data1']['lname']
            project.target_country = request.session['data1']['country']
            project.target_city = request.session['data1']['city']
            project.target_area = request.session['data1']['area']

            project.target_relationship = request.session['data2']['beneficiary']
            project.problem = request.session['data2']['problem']
            project.solution = request.session['data2']['solution']
            project.target_amount = request.session['data2']['target']
            project.expiry = request.session['data2']['expiry']
            project.save()
            del request.session['data1']
            del request.session['data2']
            return redirect('gofund')




