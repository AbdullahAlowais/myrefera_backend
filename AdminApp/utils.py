from django.core.mail import send_mail
from django.conf import settings
import requests
from CampaignApp.models import *
from django.http.response import JsonResponse
import stripe
from django.db.models import Sum

def send_forget_password_mail(email,token):

    subject="your forget password link"
    message=f'Hi,click on the link to reset your passord http://127.0.0.1:8000/isadmin/change_password_link/{email}/{token}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)
    return True


def adminnotification(request):
    
    notification_obj=Notification.objects.filter(send_notification__in=[2,4])
    
    notify_list=[]
    for i in notification_obj:
        if i.send_notification==2:
            
            dict={
                "message": i.influencerid.username + " accepted your campaign -"  + ":" +  i.campaignid.campaign_name
            }
            notify_list.append(dict["message"])
        else:
            dict={
                "message": i.influencerid.username + " declined your campaign -"  + ":" +  i.campaignid.campaign_name
            }
        
            notify_list.append(dict["message"])    
  
    return JsonResponse({"notify_list":notify_list})
 


def refund_money(request,charge,amount):
    stripe.api_key  = settings.STRIPE_API_KEY
    status_val=stripe.Refund.create(
    charge=charge,
    amount=amount
    )
    
 
    return status_val


def balance():
    total_commision_earned=FeePaid.objects.filter(campaign_id__campaign_status=2).aggregate(Sum("adminfee"))
    total_money_transfer=FeePaid.objects.filter(campaign_id__campaign_status=2).aggregate(Sum("influ_amount"))
    
    total_balance=FeePaid.objects.filter(campaign_id__campaign_status=2).aggregate(Sum("amount"))
  
   
   
    return total_commision_earned,total_money_transfer,total_balance