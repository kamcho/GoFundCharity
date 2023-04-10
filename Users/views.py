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
from Payments.models import StripeCardPayments

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



class ProjectDetail(DetailView):
    template_name='Users/projectid.html'
    context_object_name='project'
    model=Project
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        user = self.request.user
        print(type(user))
        context['donations'] =StripeCardPayments.objects.filter(project_id=self.kwargs['pk']).count()

        print(context)
        return context

    def post(self,request,*args,**kwargs):
        if request.method=="POST":
            choice=request.POST.get('line')
            print(choice)
            request.session['project-id']=self.kwargs['pk']
            print(request.session['project-id'])

            if choice=='Card':
                return redirect('stripe-pay')
            else:
                return redirect('deposit')



import requests
from django.conf import settings
from django.views.generic import TemplateView
import stripe

stripe.api_key = "sk_test_51MrhGPHSDxMMHnYTxwz5LLK9vGRHde981TLoCjmE9HNOmtbvAlIZbn9eCk29JFq98zziGrwKOxfj1ol5N9TDEOHo00eHUdjtjw"


        


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




