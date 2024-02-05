from django.db import models
from AdminApp.models import *


# Create your models here.
class   Campaign(models.Model):
  CHOICES=(
      ("1","Marketplace"),
      ("2","Influencer")
    )
  CAMP_CHOICES=(
      ("0","Inactive"),
      ("1","Active")
    )

  vendorid=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
  influencerid=models.ForeignKey(User,related_name='influencer',on_delete=models.CASCADE,null=True)
  campaign_name=models.CharField(max_length=255,default="")
  influencer_visit=models.CharField(max_length=255,null=True,blank=True)
  offer=models.CharField(max_length=255,null=True)
  influencer_name=models.CharField(max_length=255,default="")
  date=models.DateField(null=True)
  created_at = models.DateTimeField(auto_now_add=True,null=True)
  updated_at =  models.DateTimeField(auto_now=True)
  status=models.IntegerField(default=0,choices=CHOICES)
  description=models.TextField(default="")
  campaign_status= models.IntegerField(default=0,choices=CAMP_CHOICES) 
  draft_status=models.BooleanField(default=0)
  influencer_fee=models.FloatField(blank=True,null=True)
  campaign_exp=models.BooleanField(default=True)
  end_date=models.DateField(null=True)
  payout_amount=models.IntegerField(blank=True,null=True)
  image = models.ImageField(upload_to="camp_images/",blank=True,null=True)
  
  
class Productdetails(models.Model):
  vendorid=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
  product_id=models.CharField(max_length=255,default="")
  
  


class RequestSent(models.Model):
  vendorid=models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
  campaignid=models.ForeignKey(Campaign,on_delete=models.CASCADE,blank=True)
  influencee=models.CharField(max_length=200,null=True)
  status=models.BooleanField(default=0)
  


class ModashInfluencer(models.Model):
    username = models.CharField(max_length=255,default="")
    follower = models.BigIntegerField()
    image = models.ImageField(default="",max_length=500,blank=True)
    engagements = models.BigIntegerField(null=True)
    engagement_rate=models.FloatField()
    fullname = models.CharField(max_length=255,default="")
    isverified = models.BooleanField(null=True)
    influencerid=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    admin_approved=models.BooleanField(default=0)
    paid_status=models.BooleanField(default=0)

    
    
class Product_information(models.Model):
  vendor=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
  campaignid=models.ForeignKey(Campaign,on_delete=models.CASCADE,blank=True,null=True)
  product_name=models.CharField(max_length=255,null=True)
  product_id=models.BigIntegerField(null=True)
  coupon_name=models.TextField(blank=True,null=True)
  amount=models.TextField(blank=True)
  discount_type=models.TextField(blank=True)
  coupon_id=models.TextField(blank=True,null=True)
  
  
class Campaign_accept(models.Model):
    influencerid=models.ForeignKey(User,related_name='influencer_accept',on_delete=models.CASCADE,null=True)
    campaignid=models.ForeignKey(Campaign,on_delete=models.CASCADE,null=True)
    campaign_status=models.IntegerField(default=0)
    vendor=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    modashinfluencer=models.IntegerField(null=True,blank=True)
    
    
    
class VendorCampaign(models.Model):
  influencerid=models.ForeignKey(ModashInfluencer,on_delete=models.CASCADE,blank=True,null=True)
  campaignid=models.ForeignKey(Campaign,on_delete=models.CASCADE,null=True)
  campaign_status=models.IntegerField(default=0)
  vendor=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
  
  
class Notification(models.Model):
  influencerid=models.ForeignKey(ModashInfluencer,on_delete=models.CASCADE,blank=True,null=True)
  send_notification=models.IntegerField(default=0)
  vendor=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
  campaignid=models.ForeignKey(Campaign,on_delete=models.CASCADE,null=True)
  message=models.TextField(default="")
  created_at = models.DateTimeField(auto_now_add=True,null=True)

  
  
class VendorStripeDetails(models.Model):
    vendor=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    publishable_key=models.CharField(max_length=255,blank=True)
    secret_key=models.CharField(max_length=255,blank=True)
    
   
  
class PaymentDetails(models.Model):
  amount=models.FloatField(blank=True,null=True)
  amountpaid=models.FloatField(blank=True,null=True)
  influencer=models.ForeignKey(ModashInfluencer,on_delete=models.CASCADE,blank=True,null=True)
  vendor=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
  admin=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="adminpayment")
  sales=models.FloatField(blank=True,null=True)
  influencerfee=models.FloatField(blank=True,null=True)
  offer=models.CharField(max_length=200,blank=True,null=True)
  campaign=models.ForeignKey(Campaign,on_delete=models.CASCADE,blank=True,null=True)
  account_id=models.CharField(max_length=200,blank=True,null=True)
  salespaid=models.FloatField(blank=True,null=True)
  
  
class transferdetails(models.Model):
  transferid=models.CharField(max_length=200,blank=True,null=True)
  influencer=models.ForeignKey(ModashInfluencer,on_delete=models.CASCADE,blank=True,null=True)
  vendor=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
  amount=models.IntegerField(blank=True,null=True)
  destination=models.CharField(max_length=255,blank=True,null=True)
  remaining_amount=models.FloatField(blank=True,null=True)
  campaign=models.ForeignKey(Campaign,on_delete=models.CASCADE,blank=True,null=True)
  admin=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="admin")

  
  
  
class StripeSubscription(models.Model):
  vendor=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
  status=models.BooleanField(default=False)
  subscription_id=models.CharField(blank=True,null=True,max_length=255)
  price_id=models.CharField(blank=True,null=True,max_length=255)
  start_date = models.DateField(blank=True, null=True)
  end_date = models.DateField(blank=True, null=True)
  amount=models.CharField(blank=True,null=True,max_length=255)
  
  
class CampaignCredit(models.Model):
  total_campaign=models.IntegerField(blank=True,null=True)
  status=models.BooleanField(default=False)
  used_campaign=models.IntegerField(blank=True,null=True)
  vendor=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
  start_date = models.DateField(blank=True, null=True)
  end_date = models.DateField(blank=True, null=True)
  
  


class InfluencerPaid(models.Model):
  status=models.BooleanField(default=False)
  influecerid=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
  vendorid=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True, related_name='user')


class FeePaid(models.Model):
  amount=models.IntegerField(blank=True,null=True)
  influecerid=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
  vendorid=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True, related_name='vendorpaid')
  adminfee=models.IntegerField(blank=True,null=True)
  charge_id=models.CharField(blank=True,null=True,max_length=255)
  status = models.BooleanField(default=False)
  influ_amount = models.CharField(max_length=255,default=0)
  campaign_id=models.ForeignKey(VendorCampaign,on_delete=models.CASCADE,blank=True,null=True)