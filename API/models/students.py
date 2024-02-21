from django.db import models
from django.contrib.postgres.fields import ArrayField
from .courses import Courses


class Students(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=30,blank=True, default='')
    password = models.CharField(max_length=400)
    profileImage = models.URLField(max_length=250,blank=True, default='')
    billinginfo = models.CharField(max_length=200,blank=True, default='')
    subscription = models.CharField(max_length=200,blank=True, default='')
    fees_amount_paid = models.CharField(max_length=30,blank=True, default='')
    payment_method = models.CharField(max_length=30,blank=True, default='')
    wishlist = ArrayField(models.CharField(max_length=50), size=10,blank=True,null=True)
    # wishlist = models.ManyToManyField(Courses)


    courses_enrolled = models.ManyToManyField(Courses)
    def __str__(self):
        return self.name