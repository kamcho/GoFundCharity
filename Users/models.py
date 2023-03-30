import datetime
import uuid
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.''
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
  

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
  
            # =ref
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    country=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    area=models.CharField(max_length=100)
    def __str__(self):
        return f"{self.user}"

class Project(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    title=models.CharField(max_length=30)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    surname=models.CharField(max_length=100,blank=True)

    target_relationship=models.CharField(max_length=100,blank=True)
    target_country=models.CharField(max_length=100,blank=True)
    target_city=models.CharField(max_length=100,blank=True)
    target_area=models.CharField(max_length=100,blank=True)
    problem=models.TextField(max_length=500,blank=True)
    solution=models.TextField(max_length=300,blank=True)
    target_amount=models.PositiveIntegerField(default=0)
    achieved_amount=models.PositiveIntegerField(default=0)
    date=models.DateTimeField(auto_now=True)
    expiry=models.CharField(max_length=100)
    status=models.CharField(max_length=10)
    def __str__(self):
        return f"{self.user}"


