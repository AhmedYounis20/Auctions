from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.utils.timezone import now

class User(AbstractUser):
    pass
class listing(models.Model):
    creator=models.CharField(default='UNKNOWN',max_length=200)
    winner=models.CharField(default='UNKNOWN',max_length=200)
    productname=models.CharField('product',max_length=200)
    productdescription=models.TextField('description',max_length=2000)
    productcategory=models.CharField('category',default='no category',max_length=200)
    product_price=models.FloatField('starting bid',default=0,null=False)
    product_image_url=models.CharField('image url',default='',max_length=500)
    active=models.BooleanField(default=True)
    creationtime=models.DateTimeField(default=now)
    def __str__(self):
        return self.productname
class comment(models.Model):
    username=models.CharField(default='UNKOWN',max_length=500)
    creationtime=models.DateTimeField(default=now)
    product=models.ForeignKey(listing, on_delete=models.CASCADE)
    comment=models.TextField(default='')
class bid(models.Model):
    product = models.ForeignKey(listing,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    bids=models.IntegerField()

class watchlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(listing,on_delete=models.CASCADE)

