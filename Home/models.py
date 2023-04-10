from django.db import models
from Users.models import MyUser
# Create your models here.

class Quizes(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    quiz = models.TextField(max_length=100)
    answer = models.TextField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    answered_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, default='pending')

    def __str__(self):
        return f"{self.user}"


class Mails(models.Model):
    names = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=50)
    mail = models.EmailField()
    quiz = models.TextField(max_length=200)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.names}"