from django.db import models
from AdminApp.models import *
from CampaignApp.models import *


# Create your models here.

class influencer_coupon(models.Model):
    influencer_id=models.ForeignKey(ModashInfluencer,on_delete=models.CASCADE,blank=True,null=True)
    vendor=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    coupon_name=models.CharField(max_length=255,blank=True,null=True)
    amount=models.FloatField(blank=True,null=True)
    coupon_id=models.CharField(max_length=255,blank=True,null=True)
    

    
class Marketplace_coupon(models.Model):
    vendor=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    coupon_name=models.CharField(max_length=255,blank=True,null=True)
    amount=models.FloatField(blank=True,null=True)
    coupon_id=models.CharField(max_length=255,blank=True,null=True)