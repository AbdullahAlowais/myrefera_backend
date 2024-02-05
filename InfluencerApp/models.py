from django.db import models
from AdminApp.models import *
from CampaignApp.models import *

# Create your models here.

class InfluencerDetails(models.Model):
    influencerid=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    industries=models.CharField(max_length=255,blank=True,null=True)
    experience=models.CharField(max_length=255,blank=True,null=True)
    promotion=models.CharField(max_length=255,blank=True,null=True)
    customer_age=models.CharField(max_length=255,blank=True,null=True)
    gender=models.CharField(max_length=255,blank=True,null=True)
    location=models.CharField(max_length=255,blank=True,null=True)
    commission=models.FloatField(blank=True,null=True)
    
   

    
    
class StripeDetails(models.Model):
    influencer=models.ForeignKey(ModashInfluencer,on_delete=models.CASCADE,blank=True,null=True)
    account_id=models.CharField(max_length=255,blank=True,null=True)
    vendor=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
