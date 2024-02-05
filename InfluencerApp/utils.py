from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six   
from rest_framework.views import APIView,View
from rest_framework import generics
from rest_framework import  status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from AdminApp.models import *                   
import stripe               
from InfluencerApp.models import *
import requests     

class TokenGen(PasswordResetTokenGenerator):  
    def _make_hash_value(self, user, timestamp):  

        return (  
            six.text_type(user.id) + six.text_type(timestamp) +  
            six.text_type(user.is_active)  
        )  
account_activation_token = TokenGen()  


class VerificationView(generics.GenericAPIView):
    def get(self,request,token,id):
        user=User.objects.get(id=id)
        if not user.verify_email:
            user.verify_email=True
            user.save()
        return Response({"Success": "Influencer Register Successfully"},status=status.HTTP_201_CREATED)
        
        
def createaccount(secret):
        stripe.api_key=secret
        account = stripe.Account.create(
        country="US",
        type="custom",
        capabilities={"card_payments": {"requested": True}, "transfers": {"requested": True},"us_bank_account_ach_payments":{"requested":True}},
        business_type="individual",
        business_profile={'mcc':'5734', 'url':'https://www.google.com/'},

        individual ={'first_name':"sood",
        'last_name':"arpan",
        'email': "test@gmail.com",
        'phone':"+15555551234",
        'ssn_last_4':"0000",
        'address':{'city':"NY", 'state':"New York", 'postal_code':10017, 'country': 'US', 'line1':"609 5th Ave"},
        'dob':{'day':11 , 'month':11 , 'year' :1999},

        },

        external_account = {'object':'bank_account',
        'country': 'US','currency': 'USD', 
        'account_number': "000123456789",
        'routing_number': "110000000",
        'account_holder_name' : "test",
        'account_holder_type': "individual"
        },
        
        tos_acceptance={"date": 1609798905, "ip": "8.8.8.8"}
        )
        return account
   
def click_analytics(request,influencer_id,serializer):
    influencer_obj = ModashInfluencer()
    dict={
    "platform": ["instagram","tiktok"],
    "influencer_id": influencer_id
    }
    headers2={"Authorization": "Bearer 1m5vdEGduXxmd4QpwpL48Xj8FiA1jxrLPwQPO0W5"}

    base_url="https://app.clickanalytic.com/api/v2/analysis"
    response=requests.post(base_url,headers=headers2,json=dict)
    
    if response.status_code==200:
        influencer_obj.follower=response.json()["user_profile"]["followers"]
        influencer_obj.engagement_rate=response.json()["user_profile"]["engagement_rate"]
        influencer_obj.engagements=response.json()["user_profile"]["engagements"]
        influencer_obj.fullname=response.json()["user_profile"]["fullname"]
        influencer_obj.username=response.json()["user_profile"]["username"]
        influencer_obj.image=response.json()["user_profile"]["picture"]
        influencer_obj.isverified=response.json()["user_profile"]["is_verified"]

        influencer_obj.save()
        
        save_obj=serializer.save(user_type =2)
        
        infl_id=serializer.data["id"]
        
        ModashInfluencer.objects.filter(id=influencer_obj.id).update(influencerid=infl_id)
        return "Created influencer"
    return "not created"