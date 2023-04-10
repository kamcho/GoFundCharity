from django.shortcuts import render
from django.views.generic import ListView,TemplateView,DetailView
from .models import Quizes,Mails
from Users.models import Profile,Project
# Create your views here.

class Home(TemplateView):
    template_name = 'Users/trade.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['charities'] = Project.objects.all()

        return context


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
    template_name = 'Users/contacts.html'

    def post(self, request):
        if request.method == "POST":
            quiz = request.POST.get('quiz')
            names = request.POST.get('names')
            location = request.POST.get('location')
            phone = request.POST.get('phone')
            mail = request.POST.get('mail')

            mail_obj = Mails.objects.create()
            mail_obj.quiz = quiz
            mail_obj.mail = mail
            mail_obj.location = location
            mail_obj.phone = phone
            mail_obj.names = names
            mail_obj.save()

            return redirect('quizes')
