from django.db import models

# Create your models here.
from Users.models import MyUser


class MpesaPayment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.TextField()
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now=True)
    transact=models.CharField(max_length=10,default="Deposit")

    def __str__(self):
        return self.user