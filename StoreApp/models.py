from django.db import models
from AdminApp.models import *
# Create your models here.


class Store(models.Model):
  userid=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
  store_name=models.CharField(max_length=255,null=True,blank=True)
  code=models.CharField(max_length=255,null=True,blank=True)
  token=models.CharField(max_length=255,blank=True,null=True)
  access_token=models.CharField(max_length=255,blank=True,null=True)
  created_at = models.DateTimeField(auto_now_add=True,null=True)
  updated_at =  models.DateTimeField(auto_now=True)