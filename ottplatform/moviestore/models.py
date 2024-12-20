from typing import Iterable
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone

class AdminLogin(AbstractBaseUser):
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(_("email address"), unique=True)
    password = models.CharField(max_length=100)
    forgotkey = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    status = models.CharField(max_length=50,default=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['password']

    objects = CustomUserManager()

    def __str__(self):
        return self.email



class MovieStore(models.Model):
    moviename = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    video = models.FileField(upload_to='videos/')
    rating = models.DecimalField(max_digits=5, decimal_places=2,default=0.0)
    view_count = models.BigIntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    
    def __str__(self):
        return self.moviename   


class Plan(models.Model):
    planname = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default=True)

  
class Watchhistory(models.Model):
    userid = models.ForeignKey(AdminLogin,on_delete=models.CASCADE,null=True)
    movieid = models.ForeignKey(MovieStore,on_delete=models.CASCADE,null=True)
    date = models.DateTimeField(default=timezone.now)


class Subscribers(models.Model):
    userid = models.ForeignKey(AdminLogin,on_delete=models.CASCADE,null=True)
    planid = models.ForeignKey(Plan,on_delete=models.CASCADE,null=True)
    startdate = models.DateField(default=timezone.now)
    enddate = models.DateField()
    year = models.PositiveIntegerField(blank=True,null=True)
    month = models.PositiveIntegerField(blank=True,null=True)
    paymentid = models.CharField(max_length=50)
    status = models.CharField(max_length=50,default=True)
    def save(self, *args, **kwargs):
        if self.startdate:
            self.year = self.startdate.year
            self.month = self.startdate.month
        super().save(*args, **kwargs)    










