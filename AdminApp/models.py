from django.db import models
from AdminApp.manager import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(AbstractBaseUser,PermissionsMixin):
    CHOICES=(
      ("2","Influencer"),
      ("3","Vendor")
    )
    username  = models.CharField(max_length=30,default="")
    email 		= models.EmailField(_('email'),unique=True)
    password    = models.CharField(max_length=255,default="")
    is_staff 	= models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')
    is_active 	= models.BooleanField(default=True,
		help_text='Designates whether this user should be treated as active.\
		Unselect this instead of deleting accounts.')
    user_type = models.CharField(default="",max_length=30,choices=CHOICES)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at =  models.DateTimeField(auto_now=True)
    country= models.CharField(max_length=30,blank=True,null=True)
    shopify_url=models.CharField(max_length=100,blank=True,null=True,unique=True)
    instagram_url=models.CharField(max_length=100,blank=True,null=True)
    category=models.CharField(max_length=255,blank=True,null=True)
    image=models.ImageField(null=True,blank=True)
    user_handle=models.CharField(max_length=30,blank=True,null=True)
    verify_email=models.BooleanField(default=False)
    vendor_status=models.BooleanField(default=True)
    fee=models.FloatField(blank=True,null=True)
    bank_account=models.CharField(blank=True,max_length=100,null=True)
    customer_id=models.CharField(blank=True,null=True,max_length=200)
    facility=models.CharField(blank=True,null=True,max_length=255)
    commission=models.FloatField(blank=True,null=True,default=0)
    phone_number = models.CharField(blank=True,null=True,max_length=255)
    USERNAME_FIELD 	='email'
    
    objects 		= CustomUserManager()
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email



class   stripe_details(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
  account_id=models.CharField(max_length=255,blank=True,null=True)
  vendor=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="vendor")

  

class commission_charges(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
  commission=models.FloatField(blank=True,null=True)