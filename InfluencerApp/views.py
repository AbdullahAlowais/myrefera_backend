from InfluencerApp.serializer import *
from InfluencerApp.models import *
from rest_framework.views import APIView,View
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from AdminApp.views import *
from CampaignApp.serializer import *
import requests
import json
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.core.mail import EmailMessage  
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from .utils import account_activation_token,VerificationView,createaccount
from django.db.models import Q
from django.core.mail import send_mail as sm
import stripe
from Affilate_Marketing import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from ShopifyApp.models import *



stripe.api_key = settings.STRIPE_API_KEY
lean_headers={"lean-app-token":"9de351e4-0240-498d-8d8a-c6b8a46de475"}

headers={"Authorization": "Bearer yGrFqiK4YqDtqODbGRZkZrWRIgsjFLZP"}


#REGISTER INFLUENCER API
"""API FOR INFLUENCER REGISTER"""
class Register(APIView):
    def post(self,request):
        influencer_id=request.data.get("user_handle")
        bank_id=request.data.get("bankname")
      
        serializer=InfluencerSerializer(data=request.data)
        if serializer.is_valid():
            

            serializer2=StepTwoSerializer(data=request.data)
            if serializer2.is_valid(raise_exception=True):

                #------------------------------------
                
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
                #-------------------------------------------    
                   
                    save_obj=serializer.save(user_type =2,bank_account=bank_id)

                #-------------------------------------------    

                    infl_id=serializer.data["id"]
                    
                    ModashInfluencer.objects.filter(id=influencer_obj.id).update(influencerid=infl_id)


                
                else:
                    return Response({"error": response.json()},status=status.HTTP_400_BAD_REQUEST)
                serializer2.save(influencerid_id=serializer.data["id"])

                #-------------------------------------------    

            
                uid64=urlsafe_base64_encode(force_bytes(serializer.data["id"]))
                current_site_info = get_current_site(request)  
                
                link=reverse('activate',kwargs={"id":serializer.data["id"],'token':account_activation_token.make_token(save_obj)})

                activate_url=str(current_site_info) + str(link)
                activate_url="https://myrefera.com/#/verify/"+ account_activation_token.make_token(save_obj)+"/"+ str(serializer.data["id"])
                html_message = render_to_string('acc_active_email.html', {
                'button_text': 'Verify Account',
                'button_link': activate_url
                })
               
                email_body=  strip_tags(html_message)
                mail_subject = 'Activate your Account'  
            
        
                to_email =serializer.data["email"]  
                email = EmailMultiAlternatives(  
                            mail_subject, email_body, to=[to_email]  
                )  
                email.attach_alternative(html_message, 'text/html')
                email.send()  
                 
                return Response({"Success":"User Created ","token":account_activation_token.make_token(save_obj),"id":serializer.data["id"]},status=status.HTTP_201_CREATED)
         

            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
"""API TO SAVE INFLUENCER DATA IN DATABASE"""
class StepOneAPIView(APIView):
    def post(self, request):
        serializer = InfluencerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
          
            
            handle = serializer.data["user_handle"]
            influencer_obj = ModashInfluencer()
            base_url = f"https://api.modash.io/v1/instagram/profile/@{handle}/report"
            response = requests.get(base_url, headers=headers)
            if response.ok:
                save_obj = serializer.save(user_type=2)
                infl_id = serializer.data["id"]
                request.session["id"] = infl_id
                influencer_data = response.json()["profile"]["profile"]
                influencer_obj.username = influencer_data["username"]
                influencer_obj.fullname = influencer_data["fullname"]
                influencer_obj.isverified = influencer_data["isVerified"]
                influencer_obj.follower = influencer_data["followers"]
                influencer_obj.image = influencer_data["picture"]
                influencer_obj.engagements = influencer_data["engagements"]
                influencer_obj.engagement_rate = round(influencer_data["engagementRate"], 2)
                influencer_obj.influencerid_id = infl_id
                influencer_obj.save()
                request.session["id"] = infl_id
            else:
                return Response(
                    {"error": response.json()},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response({"id": infl_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
"""API TO VERIFY INFLUENCER BY EMAIL LINK"""    
class StepTwoAPIView(APIView):
    def post(self, request):
        infl_id = request.session.get("id")
        if infl_id:
            influencer_obj = ModashInfluencer.objects.get(id=13)
            serializer = StepTwoSerializer(data=request.data)
        else:
            serializer = StepTwoSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(influencerid_id=72)

            # Send verification email
            infl_id = serializer.data["influencerid"]
            save_obj = User.objects.get(id=infl_id)

          
            uid64 = urlsafe_base64_encode(force_bytes(infl_id))
            current_site_info = get_current_site(request)
            activate_url = (
                "https://myrefera.com/#/verify/"
                + account_activation_token.make_token(save_obj)
                + "/"
                + str(infl_id)
            )
            email_body = (
                "Hi "
                + save_obj.username
                + ", please use this link to verify your account:\n"
                + activate_url
            )
            
            mail_subject = "Activate your Account"
            to_email = save_obj.email
            email = EmailMessage(mail_subject, email_body, to=[to_email])
            email.send()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""API TO SAVE INFLUENCER IN DATABASE"""
class Details(APIView):
    def post(self,request):
        serializer=StepTwoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(influencerid_id=request.session["id"])
            return Response({"Success": "Next Step"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    
#LOGIN INFLUENCER API  
"""API FOR INFLUENCER LOGIN"""
class InfluencerLogin(APIView): 
    def post(self, request):
        username = request.data.get('email')
        password = request.data.get('password')
    
        user = authenticate(username=username, password=password)
        
        if user: 
                
            login(request, user)
        
            if user.verify_email == True:
                usr=Token.objects.filter(user_id=user.id)
                if not usr:
                    refresh=Token.objects.create(user=user)
                    return Response({'Success':"Login Successfully",'Token':str(refresh),"username":user.username}, status=status.HTTP_200_OK)
                
                else:
                    user_key=Token.objects.filter(user_id=user.id).values_list("key",flat=True)[0]
                    if user:
            
                            return Response({'Success':"Login Successfully",'Token':str(user_key),"username":user.username}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Your email is not verified'}, status=status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
            
            
           
           
#SHOW LIST OF INFLUENCER API
"""API TO SHOW LIST OF INFLUENCER"""
class InfluencerList(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):   
        infu_list=User.objects.filter(user_type =2)
        serializer = InfluencerSerializer(infu_list,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)
    




    
    
#UPDATE INFLUENCER DATA API   
"""API TO UPDATE INFLUENCER"""
class UpdateInfluencer(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self,request,pk):
        try:
            influencer = User.objects.get(pk = pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=UpdateInfluencerSerializer(influencer,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
#ACCEPT CAMPAIGN API
"""API TO ACCEPT CAMPAIGN"""
class AcceptView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]    
    def post(self,request,id):
        try:
          
            influencer_data=Campaign.objects.filter(id=id).values_list("vendorid",flat=True)
            vendor=influencer_data[0]
            modash_data1=ModashInfluencer.objects.filter(influencerid_id=self.request.user.id).values_list("id",flat=True)
            if modash_data1:
                camp_accept=Campaign.objects.filter(id=id).update(campaign_status=1)
                infl_accept=Notification.objects.filter(campaignid_id=id,influencerid_id=modash_data1[0]).update(send_notification=2)
                cam_obj2=Campaign_accept.objects.create(influencerid_id=self.request.user.id,campaignid_id=id,campaign_status=1,vendor_id=vendor,modashinfluencer=modash_data1[0])
                influencer_data2=VendorCampaign.objects.filter(campaignid=id,influencerid_id=modash_data1[0]).update(campaign_status=2)

            cam_obj2=Campaign.objects.filter(id=id).values_list("vendorid__email",flat=True)
            
            if cam_obj2:
                email=cam_obj2[0]
         
            res = sm(
            subject = 'Campaign Accepted',
            message = 'Your Campaign is accepted by '+self.request.user.username,
            from_email = 'testsood981@gmail.com',
            recipient_list = [email],
            fail_silently=False,
        )
            
            return Response({"message":"Campaign Accepted"},status=status.HTTP_200_OK)
        except:
            return Response({"error":"Issue in Campaign"},status=status.HTTP_400_BAD_REQUEST)
    
    
#DECLINE CAMPAIGN API
"""API TO DECLINE CAMPAIGN"""
class DeclineView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]    
    def post(self,request,id):
        try:
            influencer_data=Campaign.objects.filter(id=id).values_list("vendorid",flat=True)
            vendor=influencer_data[0]
           
            modash_data1=ModashInfluencer.objects.filter(influencerid_id=self.request.user.id).values_list("id",flat=True)
            if modash_data1:
                camp_accept=Campaign.objects.filter(id=id).update(campaign_status=3)
                infl_accept=Notification.objects.filter(campaignid_id=id,influencerid_id=modash_data1[0]).update(send_notification=4)

                infl_accept=VendorCampaign.objects.filter(campaignid_id=id,influencerid_id=modash_data1[0]).update(campaign_status=4)
                cam_obj2=Campaign_accept.objects.create(influencerid_id=self.request.user.id,campaignid_id=id,campaign_status=3,vendor_id=vendor)            
          
            return Response({"message":"Campaign Decline by Influencer"},status=status.HTTP_200_OK)
        except:
            
            return Response(status=status.HTTP_400_BAD_REQUEST)




#LIST OF CAMPAIGN API
"""API TO SHOW LIST OF REQUESTED CAMPAIGN"""
class PendingCampaing(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]    
    def get(self,request):   
        try:
            campaign_list=Campaign.objects.filter(status=0)
            serializer = CampaignSerializer(campaign_list,many=True)
            return Response({"data":serializer.data},status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    
#LOGOUT API
"""API FOR LOGING OUT INFLUENCER"""
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=204)
    
    
""" API TO GET PENDIND CAMPAIGN LIST """    
class PendingList(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        lst=[]
        final_lst=[]
        res=[]
        res2=[]    
        value=ModashInfluencer.objects.filter(influencerid_id=self.request.user.id).values_list("id",flat=True)[0]
    
        vendor_codes=VendorCampaign.objects.filter(influencerid_id=value,campaign_status=0)
      
        if vendor_codes.exists():
            res.append(vendor_codes)
        else:
            res=""
        
        if res:
            
            for i in res:
                z=(i.values("campaignid"))
                res2.append(z)
        
  
            for i in res2:
                ids = [q['campaignid'] for q in i]
                for id in ids:
                    lst.append(id)
                    
        set_data=set(lst)
     
        fin_value=set_data
        for i in fin_value:
         
            camp=Product_information.objects.filter(campaignid_id=i).values()
            campaign_obj59=Product_information.objects.filter(campaignid_id=i).select_related("campaignid")
        
            for k in campaign_obj59:
               pass

        
            for i in range(len(camp)):
                cop=(camp[i]["coupon_name"])
                amt=(camp[i]["amount"])
             
                if cop:
                  
                    couponlst=ast.literal_eval(cop)
                else:
                    couponlst=cop
                    
                if amt:
                    
                    amtlst=ast.literal_eval(amt)
                else:
                    amtlst=amt
                    
               
            
                dict1={
                    "campaignid_id":camp[i]["campaignid_id"],
                    "campaign_name": k.campaignid.campaign_name ,
                    "vendor_name":k.vendor.username,
                    "status":k.campaignid.campaign_status,
                    "product":[{
                    "product_name":camp[i]["product_name"],
                    "coupon_name":couponlst,
                    "amount":amtlst,
                    "product_id": camp[i]["product_id"],
                    
                }]
                }
                final_lst.append(dict1)
                    
    
        result={}
        for i, record in enumerate(final_lst):
         
            if record["campaignid_id"] in result:
                result[record["campaignid_id"]]["product"].append(record["product"][0])
            else:
               
                result[record["campaignid_id"]] = record
                result[record["campaignid_id"]]["product"] = record["product"]
        val=list(result.values())
        sorted_val = sorted(val, key=lambda x: x['campaignid_id'], reverse=True)
     
        return Response({"data":sorted_val},status=status.HTTP_200_OK)  
    

    
    
# GET CAMPAIGN APPROVAL LIST  
"""API TO GET APPROVAL LIST"""
class ApprovalList(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = []
    def get(self,request):
        lst=[]
        final_lst=[]
        res=[]                                                                   
        res2=[]  

        value=ModashInfluencer.objects.filter(influencerid_id=request.user.id).values_list("id",flat=True)[0]
        vendor_codes=VendorCampaign.objects.filter(campaign_status=1,influencerid_id=value,campaignid__status=2)
        vendor_codes2=VendorCampaign.objects.filter(campaign_status=2,influencerid_id=value,campaignid__status=2)
        vendor_acc=vendor_codes2.values_list("campaignid_id__id",flat=True)
        vendo_camp=vendor_codes.values_list("campaignid_id__id",flat=True)
  
        campaign_obj1=Campaign_accept.objects.filter(Q(campaign_status=1)|Q(campaign_status=2),Q(influencerid_id=self.request.user.id,campaignid__status=2))
        
        if campaign_obj1.exists():
            res.append(campaign_obj1)
        else:
            res=""
        
        if res:
            
            for i in res:
                z=(i.values("campaignid"))
                res2.append(z)
        
  
            for i in res2:
                ids = [q['campaignid'] for q in i]
                for id in ids:
                    lst.append(id)
                    
        set_data=set(lst)
        
        fin_value=set_data
        for i in fin_value:
         
            camp=Product_information.objects.filter(campaignid_id=i).values()
            campaign_obj59=Product_information.objects.filter(campaignid_id=i).select_related("campaignid")
            campaign_obj595=Campaign.objects.prefetch_related("product_information_set").last()
            coupon_match=influencer_coupon.objects.filter(influencer_id=value).values_list("coupon_name",flat=True)
            
            for k in campaign_obj59:
               pass

        
            for i in range(len(camp)):
                cop=(camp[i]["coupon_name"])
              
                amt=(camp[i]["amount"])

                disc_type=(camp[i]["discount_type"])
            
                if disc_type:
                    discc_type=ast.literal_eval(disc_type)
                else:
                    
                    discc_type=disc_type
                
                if cop:
                  
                    couponlst=ast.literal_eval(cop)
                    
                    for cop in couponlst:
                        
                        if cop  not in coupon_match:
                            couponlst.remove(cop)
                            
        
                else:
                    couponlst=cop
                 
                    
                if amt:
                    
                    amtlst=ast.literal_eval(amt)
                else:
                    amtlst=amt
                    
               
               
                
                if camp[i]["campaignid_id"] in vendo_camp:
                    
                    dict1={
                        "campaignid_id":camp[i]["campaignid_id"],
                        "campaign_name": k.campaignid.campaign_name ,
                        "status":1,
                        "vendor_name":k.vendor.username,
                        "product":[{
                        "product_name":camp[i]["product_name"],
                        "coupon_name":couponlst,
                        "amount":amtlst,
                        "product_id": camp[i]["product_id"],
                        "discount_type":discc_type, 
                        
                        
                    }]
                    }
                    final_lst.append(dict1)
                    
                    
                elif camp[i]["campaignid_id"] in vendor_acc:
                    
                    dict1={
                        "campaignid_id":camp[i]["campaignid_id"],
                        "campaign_name": k.campaignid.campaign_name ,
                        "status":2,
                        "vendor_name":k.vendor.username,
                        "product":[{
                        "product_name":camp[i]["product_name"],
                        "coupon_name":couponlst,
                        "amount":amtlst,
                        "product_id": camp[i]["product_id"],
                        "discount_type":discc_type, 
                        
                        
                    }]
                    }
                    final_lst.append(dict1)
                else:
                     dict1={
                        "campaignid_id":camp[i]["campaignid_id"],
                        "campaign_name": k.campaignid.campaign_name ,
                        "status":4,
                        "product":[{
                        "product_name":camp[i]["product_name"],
                        "product_id": camp[i]["product_id"],
                        
                    }]
                    }
                     final_lst.append(dict1)
               
               
      
        result={}
        for i, record in enumerate(final_lst):
         
            if record["campaignid_id"] in result:
                result[record["campaignid_id"]]["product"].append(record["product"][0])
            else:
               
                result[record["campaignid_id"]] = record
                result[record["campaignid_id"]]["product"] = record["product"]
        val=list(result.values())
        

        
        sorted_val = sorted(val, key=lambda x: x['campaignid_id'], reverse=True)
       
        return Response({"data":sorted_val},status=status.HTTP_200_OK)  
    
    
    
#API TO GET SINGLE CAMPAIGN
"""API HELPS US TO GET SINGLE CAMPAIGN DETAILS"""
class GetCampaign(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]  
    def get(self,request,id ):
        value_lst=[]
        try:
            camp=Product_information.objects.filter(campaignid_id=id).values()
            campaign_obj=Product_information.objects.filter(campaignid_id=id).select_related("campaignid")
          

        except Campaign.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        for k in campaign_obj:
            pass
        for i in range(len(camp)):
            cop=(camp[i]["coupon_name"])
            amt=(camp[i]["amount"])
            
            if cop:
                
                couponlst=ast.literal_eval(cop)
            else:
                couponlst=cop
                
            if amt:
    
                amtlst=ast.literal_eval(amt)
            else:
                amtlst=amt
                   
            dict1={
                "campaignid_id":camp[i]["campaignid_id"],
                "product_name":camp[i]["product_name"],
                "campaign_name": k.campaignid.campaign_name ,
                "influencer_visit": k.campaignid.influencer_visit ,
                "influencer_name": k.campaignid.influencer_name ,
                "offer": k.campaignid.offer ,
                "date": k.campaignid.date ,
                "description": k.campaignid.description,
                "influencer_fee": k.campaignid.influencer_fee,
                "campaign_status":k.campaignid.campaign_status,
                "draft_status":k.campaignid.draft_status,
                "product":[{
                    "product_name":camp[i]["product_name"],
                    "name":couponlst,
                    "amount":amtlst,
                    "product_id": camp[i]["product_id"],
                }]
            }

            value_lst.append(dict1)
            
        result = {}
        for i, record in enumerate(value_lst):
         
            if record["campaign_name"] in result:
                result[record["campaign_name"]]["product"].append(record["product"][0])
            else:
               
                result[record["campaign_name"]] = record
                result[record["campaign_name"]]["product"] = record["product"]

        val=list(result.values())
        return Response({"data":val},status=status.HTTP_200_OK)
    
    
    
    
# GET CAMPAIGN Decline LIST  
"""API PROVIDE LIST OF DECLINED CAMPAIGN"""
class DeclinelList(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        lst=[]
        final_lst=[]
        res=[]
        res2=[]    
        campaign_obj=Campaign.objects.filter(Q(campaign_status=3),Q(influencerid_id=self.request.user.id)| Q(vendorid_id=self.request.user.id),status=2,draft_status=0)
        
        campaign_obj2=Campaign_accept.objects.filter(Q(campaign_status=3),Q(influencerid_id=self.request.user.id),campaignid__status=2)

        if campaign_obj2.exists():
            res.append(campaign_obj2)
        else:
            res=""
        
        if res:
            
            for i in res:
                z=(i.values("campaignid"))
                res2.append(z)
        

            for i in res2:
                ids = [q['campaignid'] for q in i]
               
                for id in ids:
                  
                    lst.append(id)

     
        set_data=set(lst)
        
        fin_value=set_data
        for i in fin_value:
         
            camp=Product_information.objects.filter(campaignid_id=i).values()
            campaign_obj59=Product_information.objects.filter(campaignid_id=i).select_related("campaignid")
        
            for k in campaign_obj59:
               pass

        
            for i in range(len(camp)):
                cop=(camp[i]["coupon_name"])
                amt=(camp[i]["amount"])
             
                if cop:
                  
                    couponlst=ast.literal_eval(cop)
                else:
                    couponlst=cop
                    
                if amt:
                    
                    amtlst=ast.literal_eval(amt)
                else:
                    amtlst=amt
                    
                    
                dict1={
                    "campaignid_id":camp[i]["campaignid_id"],
                    "campaign_name": k.campaignid.campaign_name ,
                    "vendor_name":k.vendor.username,
                    "product":[{
                    "product_name":camp[i]["product_name"],
                    "product_id": camp[i]["product_id"],
                }]
                }
    


                final_lst.append(dict1)
                
        result={}
        for i, record in enumerate(final_lst):
         
            if record["campaignid_id"] in result:
                result[record["campaignid_id"]]["product"].append(record["product"][0])
            else:
               
                result[record["campaignid_id"]] = record
                result[record["campaignid_id"]]["product"] = record["product"]
        val=list(result.values())

        sorted_val = sorted(val, key=lambda x: x['campaignid_id'], reverse=True)
       
        return Response({"data":sorted_val},status=status.HTTP_200_OK)  
    
    
#GET LIST OF NOTIFICATION API
"""API TO SHOW NOTIFICATION TO INFLUENCER"""
class VendorNotification(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        modash_get=ModashInfluencer.objects.filter(influencerid_id=self.request.user.id,).values_list('id',flat=True)[0]
     
        notification_obj=Notification.objects.filter(influencerid_id=modash_get,send_notification__in=[1,3,5]).values("send_notification","vendor__username","campaignid__campaign_name")
        
        notify_list=[]
        
        for i in notification_obj:
            
            if i["send_notification"]==1:
                dict={
                    "message": f'{i["vendor__username"]}' + " " + "send you request for" + " " +  f'{i["campaignid__campaign_name"]}'
                }
            
                notify_list.append(dict)
            elif i["send_notification"]==3:
                dict={
                    "message": f'{i["vendor__username"]}' +  " " + "Approved your request for"  + " " +  f'{i["campaignid__campaign_name"]}'
                }
            
                notify_list.append(dict)
            else:
                
                dict={
                    "message": f'{i["vendor__username"]}' + " " + "Decline your request for"  + " " +  f'{i["campaignid__campaign_name"]}'
                }
            
                notify_list.append(dict)
                
        return Response({"data":notify_list},status=status.HTTP_200_OK)  
    
    
#GET LIST OF NOTIFICATION API
"""API TO CHANGE NOTIFICATION STATUS"""
class ChangeNotifStatus(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        modash_get=ModashInfluencer.objects.filter(influencerid_id=self.request.user.id).values_list('id',flat=True)[0]
        notification_obj=Notification.objects.filter(influencerid_id=modash_get,send_notification__in=[1,4,3,5]).update(send_notification=0)


          
        dict={
            "message":  "Notification status updated"
        }
    
        
        return Response(dict,status=status.HTTP_200_OK)  
    
"""API TO CREATE  INFLUENCER ACCOUNT WITH STRIPE DETAILS"""
class StripeConnectAccountView(APIView):
    
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):  
        first_name=request.data.get("first_name")
        last_name=request.data.get("last_name")
        email=request.data.get("email")
        country=request.data.get("country")
        account_number=request.data.get("account_number")
        routing_number=request.data.get("routing_number")
        account_holder_name=request.data.get("account_holder_name")
        secret=request.data.get("secret")
       
        vendorids=request.data.get("vendorid")
    
        check_data=StripeDetails.objects.all()
        if check_data:
            
            modash_key=ModashInfluencer.objects.filter(influencerid=self.request.user.id).values("id")
           
            
            match_data=StripeDetails.objects.filter(influencer=modash_key[0]["id"],vendor=vendorids).exists()
            
            if match_data == True:
                return Response({"message":"Account Already exists"},status=status.HTTP_409_CONFLICT)
    
                
            else:
                try:
                    acc_data=createaccount(secret)
                   

                    val=ModashInfluencer.objects.filter(influencerid=self.request.user.id).values("id")

                    stripe_details=StripeDetails()
                    stripe_details.vendor_id=vendorids
                    stripe_details.influencer_id=val[0]["id"]
                    stripe_details.account_id=acc_data["id"]
                    stripe_details.save()
                except stripe.error.StripeError as e:
                   
                    return Response({"error":e.user_message},status=status.HTTP_400_BAD_REQUEST)
                
                return Response({"message":"Account Created",'account_id': "account"},status=status.HTTP_201_CREATED)
        try:
            acc_data=createaccount(secret)
            
            val=ModashInfluencer.objects.filter(influencerid=self.request.user.id).values("id")

            stripe_details=StripeDetails()
            stripe_details.vendor_id=vendorids
            stripe_details.influencer_id=val[0]["id"]
            stripe_details.account_id=acc_data["id"]
            stripe_details.save()
            
        except stripe.error.StripeError as e:          
            return Response({"error":e.user_message},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"Account Created",'account_id': "account"},status=status.HTTP_201_CREATED)
    



"""API TO CREATE CUSTOMER ON STRIPE"""
class CustomerCreate(APIView):
    def post(self,request):
        global account_id
        global customer_id

        customer=stripe.Customer.create(
        name="hritik",
        email="person@example.edu", 
        stripe_account=account_id,

        description="My First Test Customer (created for API docs at https://www.stripe.com/docs/api)",
        )
        customer_id=customer["id"]
        return Response({'account_id': customer}, status=status.HTTP_201_CREATED)
    

"""API TO CREATE PAYMENTINTENT"""    
class CreatePaymentIntent(APIView):
    def post(self,request):
        global account_id
        global customer_id
        payment_intent=stripe.PaymentIntent.create(amount=10000, currency="usd", transfer_group="ORDER10",stripe_account=account_id)
        return Response({'account_id': payment_intent}, status=status.HTTP_201_CREATED)
    

"""API TO CREATE STRIPE TOKEN"""    
class StripeToken(APIView):
    def post(self,request):
        global bank_account
        bank=stripe.Token.create(
        bank_account={"country": "US",      
        "currency": "usd",       
        "account_holder_name": "tester",       
        "account_holder_type": "individual",      
        "routing_number": "110000000",       
        "account_number": "000123456789", },

        )
        bank_account=bank["id"]   
        return Response({'account_id': bank}, status=status.HTTP_201_CREATED)
    
    
"""API TO VERIFY CUSTOMER ON STRIPE"""
class Stripeverify(APIView):
    def get(self,request):
        global account_id
        global customer_id
        source = stripe.Customer.retrieve_source(
            customer_id,
            bank_account,
            stripe_account=account_id
            )
        return Response({'account_id': source}, status=status.HTTP_201_CREATED)


"""CREATE LEANCUSTOMER IN SANDBOX"""
class LeanCustomer(APIView):
    def post(self,request):
        customer_name=request.data.get("customer")
        url="https://sandbox.leantech.me/customers/v1/"
        body= {"app_user_id": customer_name}
        response=requests.post(url,headers=lean_headers,json=body)
        return Response({"status":"customer created successfully","response":response.json()},status=status.HTTP_201_CREATED)
  

"""CREATE LEANENDCUSTOMER IN SANDBOX"""
class LeanEndCustomer(APIView):
    def post(self,request):
        customer_name=request.data.get("customer")
        refrence=request.data.get("refrence")
        url="https://sandbox.leantech.me/customers/v1/end-users/"
        body= {"customer_id": customer_name,"reference": refrence}
        response=requests.post(url,headers=lean_headers,json=body)
        return Response({"status":"customer created successfully","response":response.json()},status=status.HTTP_201_CREATED)
    
    
"""API TO GET CUSTOMER BY ID"""
class GetCustomer(APIView):
    def get(self,request):
        url="https://sandbox.leantech.me/customers/v1/app-user-id/arpansaini/"
        response=requests.get(url,headers=lean_headers)
        return Response({"status":"Customer data","response":response.json()},status=status.HTTP_201_CREATED)


"""API TO GET LEAN ENTITY"""
class GetEntity(APIView):
    def get(self,request):
        url="https://sandbox.leantech.me/customers/v1/46e77c5d-e010-4859-a825-9cb77165318e/entities/"
        response=requests.get(url,headers=lean_headers)
        return Response({"status":"Lean Entity","response":response.json()},status=status.HTTP_201_CREATED)
    
    
"""API TO CREATE LEANCUSTOMER """    
class LeanDestination(APIView):
    def post(self,request):
        cus_destination=request.data.get("destination")
      
        url="https://sandbox.leantech.me/payments/v1/destinations"
        body=cus_destination
        response=requests.post(url,headers=lean_headers,json=body)
        return Response({"status":"customer created successfully","response":response.json()},status=status.HTTP_201_CREATED)


"""API TO GET LEAN DESTINATION"""
class DestinationList(APIView):
    def get(self,request):
       
        url="https://sandbox.leantech.me/payments/v1/destinations/be2033db-f6e0-4914-a8a0-ab80027262e7/"
        response=requests.get(url,headers=lean_headers)
        return Response({"status":"customer created successfully","response":response.json()},status=status.HTTP_201_CREATED)



"""API TO GET PAYMENT LIST"""
class PaymentList(APIView):
    def get(self,request):  
        url="https://sandbox.leantech.me/customers/v1/61023285-db5e-4a84-826c-6cec68f06cc5/payment-sources/"
        response=requests.get(url,headers=lean_headers)
        return Response({"status":"customer created successfully","response":response.json()},status=status.HTTP_201_CREATED)



"""API TO GET BANK LIST IN LEANTECH"""
class BankList(APIView):
    def get(self,request):
        url="https://sandbox.leantech.me/banks/v1/"
        response=requests.get(url,headers=lean_headers)   
        return Response({"status":"List of Banks","response":response.json()},status=status.HTTP_201_CREATED)
    

"""API TO GET PAYMENT INTENTIST LIST"""    
class PaymnetIntentist(APIView):
    def get(self,request):
        url="https://sandbox.leantech.me/payments/v1/intents/ffaf421c-7eeb-475e-8f2f-fc3f080a50a7/"
      
        response=requests.get(url,headers=lean_headers)   
     
        return Response({"status":"List of Banks","response":response.json()},status=status.HTTP_201_CREATED)


"""API TO VERIFY NAME IN LEAN PAYMEN GATEWAY"""
class VerifyName(APIView):
    def get(self,request):
        dict1={"entitiy_id":"e5780913-adc5-4488-bde4-8ef30e414898",
               "customer":"arpansaini"}
        url="https://sandbox.leantech.me/insights/v1/name-verification/"
     
        response=requests.post(url,headers=lean_headers)   
     
        return Response({"status":"verify_name","response":response.json()},status=status.HTTP_201_CREATED)

# class LeanPayment(APIView):
    
#     def post(self,request):
#     #     js="""function LeanPayment()
#     #         Lean.connect({
#     #         app_token: "YOUR_APP_TOKEN",
#     #         customer_id: "CUSTOMER_ID",
#     #         permissions: ["payments"],
#     #         payment_destination_id: "SEBASTIANS_DESTINATION_ID", //make sure to include the beneficiary's destination ID or else the default destination (Company's CMA account) will be linked
#     #         sandbox: true
#     #     })
#     #     const value=LeanPayment();
        
#     #     """
#     #     context=js2py.eval_js()
#     #     context.execute
#     #     return Response({"status":"hello"})



def value(request):
    return render(request,"script.html")


"""API TO SAVE INFLUENCER STRIPE DETAILS"""
class InfluencerStripe(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        seri_obj=StripeSerializer(data=request.data)
        if seri_obj.is_valid(raise_exception=True):
            seri_obj.save(influencer_id=self.request.user.id)
            return Response({"success":" Stripe Details Saved Successfully"},status=status.HTTP_201_CREATED)
        return Response({"error":seri_obj.error_messages},status=status.HTTP_201_CREATED)
    
    
    
    
"""API TO CREATE CONNECTED ACCOUNT IN STRIPE"""    
class CreateConnectedAccountView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CreateConnectedAccountSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        bank_account_token = serializer.validated_data.get('bank_account_token')
        platform_account_id = serializer.validated_data.get('platform_account_id')

        try:
            account = stripe.Account.create(
                type='standard',
                email=email,
                capabilities={
                    'card_payments': {'requested': True},
                    'transfers': {'requested': True},
                },
                country='AE', 
                business_type='individual',
                external_account=bank_account_token,
                # stripe_account=platform_account_id
            )
            
            return Response(account, status=status.HTTP_200_OK)
        except stripe.error.AuthenticationError as e:
    
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except stripe.error.APIConnectionError as e:
          
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except stripe.error.StripeError as e:
           
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
          
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""API TO CREATE STRIPE TOKEN"""
class create_bank_account_token(APIView):
    
    def post(self, request):
        serializer = BankAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        try:
            bank_account_token = stripe.Token.create(
                bank_account={
                    'account_number': data['account_number'],
                    'routing_number': data['routing_number'],
                    'currency': 'aed',  
                    'country': 'AE',  
                }
            )
            
            return Response(bank_account_token, status=status.HTTP_200_OK)
          
        except stripe.error.AuthenticationError as e:
       
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except stripe.error.APIConnectionError as e:
           
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except stripe.error.StripeError as e:
         
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""API TO GET INFLUENCER DATA"""
class InfluencerData(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated] 
    def get(self,request):
        headers={'clientid':'cli_a82767c340834da9ec112207','token':'9463d65d0d1e5458ea06589e44343e45f9cff35c54552c5c13957d7116af0fdaada7420620e78b47f97f499a370898edf30019c2d87b182936c6be7c19300be1'}
        username=request.data.get("user")
        url=f"https://matrix.sbapis.com/b/instagram/statistics?query={username}"
        
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            followers=response.json()["data"]["statistics"]["total"]["followers"]
            following=response.json()["data"]["statistics"]["total"]["following"]
            engagement_rate=response.json()["data"]["statistics"]["total"]["engagement_rate"]
            username=response.json()["data"]["id"]["display_name"]
            handle_name=response.json()["data"]["id"]["username"]
            profile_pic=response.json()["data"]["general"]["branding"]["avatar"]
            verified=response.json()["data"]["misc"]["sb_verified"]
        
        
            instagram_data={
                "profile_pic":profile_pic,
                "username":username,
                "handle_name":handle_name,
                "followers":followers,
                "following":following,
                "engagement_rate":engagement_rate,
                "verified":verified,
            }
            return Response({"data":instagram_data},status=status.HTTP_200_OK)
        return Response({"error":response.json()},status=status.HTTP_400_BAD_REQUEST)
        
        

"""API TO GET ALL VENDOR STRIPE DETAILS LIST"""        
class Vendorkey(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated] 
    def get(self,request):
        try:
            
            get_key=VendorStripeDetails.objects.all().values("vendor__username","secret_key","vendor")
            key_list=[]
            for i in get_key:
                dict={
                    "vendor_key":i["secret_key"],
                    "vendor":i["vendor__username"],
                    "vendor_id":i["vendor"]
                    
                }
                key_list.append(dict)
            return Response({"data":key_list},status=status.HTTP_200_OK)

        except Exception as e:
          
            return Response({"error":"please try again"},status=status.HTTP_400_BAD_REQUEST)
            
        
        
 # try:
           
        #     account = stripe.Account.create(
        #     country="AE",
        #     type="custom",
        #     capabilities={"card_payments": {"requested": True}, "transfers": {"requested": True}},
        #     business_type="company",
        #     business_profile={'mcc':'5734', 'url':'https://www.google.com/',
        #                         "support_phone":"55-798-4597",
        #                         "product_description":"hello"},

        #     tos_acceptance={"date": 1609798905, "ip": "8.8.8.8"},
        #     company={
        #         "structure": "sole_establishment",
        #         "name": "hell334o",
        #         "phone": "555-123-4567",
        #         "tax_id": "1234",
        #         "executives_provided": False,
        #         "owners_provided": False,
        #         "directors_provided":False
        #     },
        #     representative={
        #         "first_name":"hritik"
        #     },

        #     external_account={
        #     'object': 'bank_account',
        #     'country': 'AE',
        #     'currency': 'AED',
        #     'account_number': 'AE070331234567890123456',
        #     'account_holder_name': 'test',
        #     'account_holder_type': 'individual'
        # }
        # )
            
        
"""API TO GET INFLUENCER DETAILS BY CLICK ANALYTICS"""        
class Click_analytics(APIView):
    def get(self,request):
        headers2={"Authorization": "Bearer 1m5vdEGduXxmd4QpwpL48Xj8FiA1jxrLPwQPO0W5"}
        platform=request.data.get("platform")
        
        influencer_id=request.data.get("influencer_id")
       
        
        dict={
        "platform": platform,
        "influencer_id": influencer_id
        }
       
       
        url="https://app.clickanalytic.com/api/v2/analysis"
        
        response=requests.post(url,headers=headers2,json=dict)
       
        if response.status_code==200:
            followers=response.json()["user_profile"]["followers"]
            engagement_rate=response.json()["user_profile"]["engagement_rate"]
            engagement=response.json()["user_profile"]["engagements"]
            username=response.json()["user_profile"]["fullname"]
            handle_name=response.json()["user_profile"]["username"]
            profile_pic=response.json()["user_profile"]["picture"]
            verified=response.json()["user_profile"]["is_verified"]
        
        
            instagram_data={
                "profile_pic":profile_pic,
                "username":username,
                "handle_name":handle_name,
                "followers":followers,
                "engagement":engagement,
                "engagement_rate":engagement_rate,
                "verified":verified,
            }
            return Response({"data":instagram_data},status=status.HTTP_200_OK)
        return Response({"error":response.json()},status=status.HTTP_400_BAD_REQUEST)
    
    


class Dubaiaccount(APIView):
    def post(self,request):
           
        account = stripe.Account.create(
        country="AE",
        type="custom",
        capabilities={"card_payments": {"requested": True}, "transfers": {"requested": True}},
        business_type="company",
        business_profile={'mcc':'5734', 'url':'https://www.google.com/',
                            "support_phone":"55-798-4597",
                            "product_description":"hello"},

        tos_acceptance={"date": 1609798905, "ip": "8.8.8.8"},
        company={
            "structure": "sole_establishment",
            "name": "hritrrrrrrr333r44444444444444444rik",
            "phone": "555-123-4567",
            "tax_id": "1234",
            # "executives_provided": False,
            # "owners_provided": True,
            # "directors_provided":False,    
            "address": {
            "line1": "123 Main St",
            "city": "Dubai",
            "state": "Dubai",
            "postal_code": "12345",
            "country": "AE"
             },
            
              
        },
        
       

        # representative={
        #     "first_name":"hritik"
        # },
        
        
        external_account={
        'object': 'bank_account',
        'country': 'AE',
        'currency': 'AED',
        'account_number': 'AE070331234567890123456',
        'account_holder_name': 'test',
        'account_holder_type': 'company'
        }
        )
        
        person=stripe.Account.create_person(
        account.id,
        first_name="Jane",
        last_name="Diaz",
        )
            
      
        
         
        data=stripe.Account.modify_person(
        account.id,
        person.id,
        relationship={"representative": True,"owner":True},
        
        )
       
        return Response({"detais":account})
        
        
#ADMIN DECISION
"""API TO SHOW IF ADMIN ACCEPTED YOU OR REJECT YOUR PROFILE"""
class Admindecision(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated] 
    def get(self,request):
        accept_infl=ModashInfluencer.objects.filter(influencerid=self.request.user.id,admin_approved=1)
        
        if accept_infl:
            dict={"message": "Admin Approved your Profile"}
        else:
            dict={"message": "Admin Declined your Profile"}
        return Response(dict)
    
    

""""API TO GET INFLUENCER DATA"""    
class InfluencerData(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated] 
    
    def get(self,request):
        infl_data=InfluencerDetails.objects.filter(influencerid=self.request.user.id).values("influencerid__username","influencerid__email","influencerid__country","influencerid__promotion")
        


#influencer apply
# class InfluencerApplied(APIView):
#     authentication_classes=[TokenAuthentication]
#     permission_classes = [IsAuthenticated] 
    
#     def get(self,request):
#         camp_id=request.query_params.get('value')
#         infl_ids=ModashInfluencer.objects.get(influencerid=self.request.user.id)
        
#         camp_accept=Campaign.objects.filter(id=camp_id).update(campaign_status=1)
#         infl_accept=Notification.objects.filter(campaignid_id=camp_id,influencerid_id=infl_ids.id).update(send_notification=2)

#         vendor_id=Campaign.objects.get(id=camp_id)
#         infl_ids=ModashInfluencer.objects.get(influencerid=self.request.user.id)
        
#         VendorCampaign.objects.create(campaign_status=1,campaignid_id=camp_id,influencerid_id=infl_ids.id,vendor=vendor_id.vendorid)
#         camp=Product_information.objects.get(campaignid=camp_id)
       
        
        
#         # dict1={
#         #         "campaignid_id":camp_id,
#         #         "campaign_name":camp.campaignid.campaign_name ,
#         #         "product":[{
#         #         "product_name":camp.product_name,
#         #         "coupon_name":ast.literal_eval(camp.coupon_name),
#         #         "amount":ast.literal_eval(camp.amount),
#         #         "discount_type":ast.literal_eval(camp.discount_type),
#         #         "product_id": camp.product_id,
#         #     }]
#         # }    
        
#         lst=[]
#         final_lst=[]
#         res=[]
#         res2=[]    
        
#         vendor_codes=VendorCampaign.objects.filter(influencerid_id=infl_ids.id,campaign_status=1)
       
#         if vendor_codes.exists():
#             res.append(vendor_codes)
#         else:
#             res=""
        
#         if res:
            
#             for i in res:
#                 z=(i.values("campaignid"))
#                 res2.append(z)
        
  
#             for i in res2:
#                 ids = [q['campaignid'] for q in i]
#                 for id in ids:
#                     lst.append(id)
                    
#         set_data=set(lst)
     
#         fin_value=set_data
#         for i in fin_value:
         
#             camp=Product_information.objects.filter(campaignid_id=i).values()
#             campaign_obj59=Product_information.objects.filter(campaignid_id=i).select_related("campaignid")
        
#             for k in campaign_obj59:
#                pass

        
#             for i in range(len(camp)):
#                 cop=(camp[i]["coupon_name"])
#                 amt=(camp[i]["amount"])
             
#                 if cop:
                  
#                     couponlst=ast.literal_eval(cop)
#                 else:
#                     couponlst=cop
                    
#                 if amt:
                    
#                     amtlst=ast.literal_eval(amt)
#                 else:
#                     amtlst=amt
                    
               
            
#                 dict1={
#                     "campaignid_id":camp[i]["campaignid_id"],
#                     "campaign_name": k.campaignid.campaign_name ,
                    
#                     "status":k.campaignid.campaign_status,
#                     "product":[{
#                     "product_name":camp[i]["product_name"],
#                     "coupon_name":couponlst,
#                     "amount":amtlst,
#                     "product_id": camp[i]["product_id"],
                    
#                 }]
#                 }
#                 final_lst.append(dict1)
                    
    
#         result={}
#         for i, record in enumerate(final_lst):
         
#             if record["campaignid_id"] in result:
#                 result[record["campaignid_id"]]["product"].append(record["product"][0])
#             else:
               
#                 result[record["campaignid_id"]] = record
#                 result[record["campaignid_id"]]["product"] = record["product"]
#         val=list(result.values())
        
#         return Response({"data":val},status=status.HTTP_200_OK)   



     
# class AssignCoupon(APIView):
#     authentication_classes=[TokenAuthentication]
#     permission_classes = [IsAuthenticated] 
#     def post(self,request):
#         camp_id=request.data.get("campaignid")
#         influ_id=ModashInfluencer.objects.get(influencerid=self.request.user.id)
        
#         influencer_coupon.objects.create
        
        
#influencer apply
"""API TO APPLY INFLUENCER"""        
class InfluencerApplied(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated] 
    
    def post(self,request):
       
        
        try:

            camp_id=request.query_params.get('value')        
            infl_ids=ModashInfluencer.objects.get(influencerid=self.request.user.id)
            vendors_id=Campaign.objects.get(id=camp_id)
            check=VendorCampaign.objects.filter(campaign_status=1,campaignid_id=camp_id,influencerid_id=infl_ids.id,vendor_id=vendors_id.vendorid.id).exists()
            
            if check==True:
                return Response({"success":"Already Applied"},status=status.HTTP_400_BAD_REQUEST)   
            
            camp_accept=Campaign.objects.filter(id=camp_id).update(campaign_status=1)
            infl_accept=Notification.objects.create(campaignid_id=camp_id,influencerid_id=infl_ids.id,send_notification=2,vendor_id=vendors_id.vendorid.id)
            VendorCampaign.objects.create(campaign_status=1,campaignid_id=camp_id,influencerid_id=infl_ids.id,vendor_id=vendors_id.vendorid.id)
            camp=Product_information.objects.get(campaignid=camp_id)  
            vendor_codes=VendorCampaign.objects.filter(influencerid_id=infl_ids.id,campaign_status=1)
        
            
            return Response({"success":"Successfully Applied","code":200},status=status.HTTP_200_OK)   
        except Exception as e:
            return Response({"error":e,"code":400},status=status.HTTP_200_OK)   




    
    
    
"""API TO APPLY CAMPAIGN"""    
class AppliedCampaign(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated] 
    
    def get(self,request):
        lst=[]
        final_lst=[]
        res=[]
        res2=[]    

        infl_ids=ModashInfluencer.objects.get(influencerid=self.request.user.id)
        
        vendor_codes=VendorCampaign.objects.filter(influencerid_id=infl_ids.id,campaign_status=1)
        
        if vendor_codes.exists():
            res.append(vendor_codes)
        else:   
            res=""
        
        if res:
            
            for i in res:
                z=(i.values("campaignid"))
                res2.append(z)
        
  
            for i in res2:
                ids = [q['campaignid'] for q in i]
                for id in ids:
                    lst.append(id)
                    
        set_data=set(lst)
     
        fin_value=set_data
        for i in fin_value:
         
            camp=Product_information.objects.filter(campaignid_id=i).values()
            campaign_obj59=Product_information.objects.filter(campaignid_id=i).select_related("campaignid")
        
            for k in campaign_obj59:
               pass

        
            for i in range(len(camp)):
                cop=(camp[i]["coupon_name"])
                amt=(camp[i]["amount"])
             
                if cop:
                  
                    couponlst=ast.literal_eval(cop)
                else:
                    couponlst=cop
                    
                if amt:
                    
                    amtlst=ast.literal_eval(amt)
                else:
                    amtlst=amt
                    
               
            
                dict1={
                    "campaignid_id":camp[i]["campaignid_id"],
                    
                    "campaign_name": k.campaignid.campaign_name,
                    "status":k.campaignid.campaign_status,
                    "product":[{
                    "product_name":camp[i]["product_name"],
                    "coupon_name":couponlst,
                    "amount":amtlst,
                    "product_id": camp[i]["product_id"],
                    
                }]
                }
                final_lst.append(dict1)
                    
    
        result={}
        for i, record in enumerate(final_lst):
         
            if record["campaignid_id"] in result:
                result[record["campaignid_id"]]["product"].append(record["product"][0])
            else:
               
                result[record["campaignid_id"]] = record
                result[record["campaignid_id"]]["product"] = record["product"]
        val=list(result.values())
        sorted_val = sorted(val, key=lambda x: x['campaignid_id'], reverse=True)

        return Response({"data":sorted_val},status=status.HTTP_200_OK)   

      
        
    
"""API TO GET INFLUENCER DETAILS"""    
class InfluencerProfile(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated] 


    def get(self,request):
        try:
            infl_details=User.objects.get(id=self.request.user.id)
            
            infl_dict={
                "name":infl_details.username,
                "email":infl_details.email,
                "country":infl_details.country,
                "user_handle":infl_details.user_handle
            }

            return Response({"details":infl_dict},status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error":e},status=status.HTTP_400_BAD_REQUEST)


"""API TO SHOW MARKETPLACE  ACCEPT CAMPAIGN"""
class MarketplaceAccept(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        lst=[]
        final_lst=[]
        res=[]
        res2=[]  
     
        value=ModashInfluencer.objects.filter(influencerid_id=request.user.id).values_list("id",flat=True)[0]
        vendor_codes=VendorCampaign.objects.filter(influencerid_id=value,campaign_status=2,campaignid__status=1)
        vendo_camp=vendor_codes.values_list("campaignid_id__id",flat=True)
        
        for data in vendo_camp:
           
            camp=Product_information.objects.filter(campaignid_id=data).values()
         
            campaign_obj59=Product_information.objects.filter(campaignid_id=data).select_related("campaignid")
           
            coupon_match=influencer_coupon.objects.filter(influencer_id=value).values_list("coupon_name",flat=True)
            
            
            for k in campaign_obj59:
               pass

        
            for i in range(len(camp)):
               
                cop=(camp[i]["coupon_name"])
               
                amt=(camp[i]["amount"])

                disc_type=(camp[i]["discount_type"])
            
                if disc_type:
                    discc_type=ast.literal_eval(disc_type)
                else:
                    
                    discc_type=disc_type
                
                if cop:
                  
                    couponlst=ast.literal_eval(cop)
                    
                    # for cop in couponlst:
                        
                    #     if cop  not in coupon_match:
                            
                    #         couponlst.remove(cop)
                            
        
                else:
                    couponlst=cop
                    
                 
                    
                if amt:
                    
                    amtlst=ast.literal_eval(amt)
                else:
                    amtlst=amt
                    
               
               
                if camp[i]["campaignid_id"] in vendo_camp:
                    dict1={
                        "campaignid_id":camp[i]["campaignid_id"],
                        "campaign_name": k.campaignid.campaign_name ,
                        "status":k.campaignid.campaign_status,
                        "vendor_name":k.vendor.username,
                        "product":[{
                        "product_name":camp[i]["product_name"],
                        "coupon_name":couponlst,
                        "amount":amtlst,
                        "product_id": camp[i]["product_id"],
                        "discount_type":discc_type, 
                        
                        
                    }]
                    }
                    final_lst.append(dict1)
                    
                else:
                     dict1={
                        "campaignid_id":camp[i]["campaignid_id"],
                        "campaign_name": k.campaignid.campaign_name ,
                        "status":k.campaignid.campaign_status,
                        "product":[{
                        "product_name":camp[i]["product_name"],
                        "product_id": camp[i]["product_id"],
                        
                    }]
                    }
                     final_lst.append(dict1)
               
        result={}
        for i, record in enumerate(final_lst):
         
            if record["campaignid_id"] in result:
                result[record["campaignid_id"]]["product"].append(record["product"][0])
            else:
               
                result[record["campaignid_id"]] = record
                result[record["campaignid_id"]]["product"] = record["product"]
        val=list(result.values())

        sorted_val = sorted(val, key=lambda x: x['campaignid_id'], reverse=True)
        return Response({"data":sorted_val},status=status.HTTP_200_OK)  

    
    
        
        
    

"""API TO SHOW MARKETPLACE DRAFT LIST"""    
class MarketplaceDeclinelList(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        lst=[]
        final_lst=[]
        res=[]
        res2=[]  
     
        value=ModashInfluencer.objects.filter(influencerid_id=request.user.id).values_list("id",flat=True)[0]
        vendor_codes=VendorCampaign.objects.filter(influencerid_id=value,campaign_status=4,campaignid__status=1)
        vendo_camp=vendor_codes.values_list("campaignid_id__id",flat=True)
        
        for data in vendo_camp:
           
           
            camp=Product_information.objects.filter(campaignid_id=data).values()
         
            campaign_obj59=Product_information.objects.filter(campaignid_id=data).select_related("campaignid")
           
            coupon_match=influencer_coupon.objects.filter(influencer_id=value).values_list("coupon_name",flat=True)
            
            
            for k in campaign_obj59:
               pass

        
            for i in range(len(camp)):
                cop=(camp[i]["coupon_name"])
              
                amt=(camp[i]["amount"])

                disc_type=(camp[i]["discount_type"])
            
                if disc_type:
                    discc_type=ast.literal_eval(disc_type)
                else:
                    
                    discc_type=disc_type
                
                if cop:
                  
                    couponlst=ast.literal_eval(cop)
                    
                    for cop in couponlst:
                        
                        if cop  not in coupon_match:
                            couponlst.remove(cop)
                            
        
                else:
                    couponlst=cop
                 
                    
                if amt:
                    
                    amtlst=ast.literal_eval(amt)
                else:
                    amtlst=amt
                    
               
               
                
                if camp[i]["campaignid_id"] in vendo_camp:
                    dict1={
                        "campaignid_id":camp[i]["campaignid_id"],
                        "campaign_name": k.campaignid.campaign_name ,
                        "status":k.campaignid.campaign_status,
                        "vendor_name":k.vendor.username,
                        "product":[{
                        "product_name":camp[i]["product_name"],
                        "coupon_name":couponlst,
                        "amount":amtlst,
                        "product_id": camp[i]["product_id"],
                        "discount_type":discc_type, 
                        
                        
                    }]
                    }
                    final_lst.append(dict1)
                    
                else:
                     dict1={
                        "campaignid_id":camp[i]["campaignid_id"],
                        "campaign_name": k.campaignid.campaign_name ,
                        "status":k.campaignid.campaign_status,
                        "product":[{
                        "product_name":camp[i]["product_name"],
                        "product_id": camp[i]["product_id"],
                        
                    }]
                    }
                     final_lst.append(dict1)
               
        result={}
        for i, record in enumerate(final_lst):
         
            if record["campaignid_id"] in result:
                result[record["campaignid_id"]]["product"].append(record["product"][0])
            else:
               
                result[record["campaignid_id"]] = record
                result[record["campaignid_id"]]["product"] = record["product"]
        val=list(result.values())
        sorted_val = sorted(val, key=lambda x: x['campaignid_id'], reverse=True)
       
        return Response({"data":sorted_val},status=status.HTTP_200_OK)  

            
    
"""API TO VIEW INFLUENCER SALE DATA"""    
class InfluencerSaledata(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def get(self,request): 
      
        # infl_ids=ModashInfluencer.objects.filter(influencerid=self.request.user.id).values_list("id",flat=True)
        
        # infl_main=infl_ids[0]
        
        # particular_sales=PaymentDetails.objects.filter(influencer=infl_main).values("sales","campaign__campaign_name")
        # sale=[]
        # sale_dict={}
        # for i in particular_sales:
           
        #     # sale_dict={
        #     #     "campaign_name":i.campaign.campaign_name,
        #     #     "sales":i.sales
        #     # }
        #     sale_dict={
        #         "campaign_name":i['campaign__campaign_name'],
        #         "sales":i['sales']
        #     }
        #     sale.append(sale_dict)

        sale2=[]
        sale_dict2={}
        sale=FeePaid.objects.filter(influecerid=self.request.user.id,campaign_id__campaign_status=2).values("influ_amount", "campaign_id__campaignid__campaign_name")
        for i in sale:
            sale_dict2={
                "campaign_name":i['campaign_id__campaignid__campaign_name'],
                "sales":i['influ_amount']
            }
            sale2.append(sale_dict2)
        
        return Response({"data":sale2},status=status.HTTP_200_OK)
    
    
"""API TO GET INFLUENCER PAYMENT DETAILS"""    
class AmountTransfer(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    
    def get(self,request):
        infl_ids=ModashInfluencer.objects.filter(influencerid=self.request.user.id).values_list("id",flat=True)
        
        infl_main=infl_ids[0]
        particular_sales=PaymentDetails.objects.filter(influencer=infl_main)
        sale=[]
        sale_dict={}
        for i in particular_sales:
            sale_dict={
                "campaign_name":i.campaign.campaign_name,
                "vendor_name":i.vendor.username,
                "amount_paid":i.amountpaid
            }
            sale.append(sale_dict)
            
        
        return Response({"data":sale},status=status.HTTP_200_OK)
    
 
"""API TO UPDATE INFLUENCER PROFILE""" 
class UpdateProfile(APIView):   
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self,request,id):
        try:
            influencer = User.objects.get(id = id,user_type=3)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=UpdateProfileSerializer(influencer,data=request.data)
        if serializer.is_valid():
            serializer.save(user_type=3)
            get_value=User.objects.filter(id=self.request.user.id).values("image")
            image_val=get_value[0]["image"]
            url_path=request.get_host()+"/static/image/"+ str(image_val)
            profile_val={
                "data":serializer.data,
                "url":url_path
            }
            return Response(profile_val,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

"""API TO REGISTER INFLUENCER"""
class Register1(APIView):
    def post(self,request):
        influencer_id=request.data.get("user_handle")
      
        serializer=InfluencerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            

            serializer2=StepTwoSerializer(data=request.data)
          
            if serializer2.is_valid(raise_exception=True):
                
                influencer_obj = ModashInfluencer()
                influencer_obj.follower=122
                influencer_obj.engagement_rate=12.45
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


                
                else:
                    return Response({"error": response.json()},status=status.HTTP_400_BAD_REQUEST)
                serializer2.save(influencerid_id=serializer.data["id"])
            
                uid64=urlsafe_base64_encode(force_bytes(serializer.data["id"]))
                current_site_info = get_current_site(request)  
                
                link=reverse('activate',kwargs={"id":serializer.data["id"],'token':account_activation_token.make_token(save_obj)})

                # activate_url=str(current_site_info) + str(link)
                activate_url="https://myrefera.com/#/verify/"+ account_activation_token.make_token(save_obj)+"/"+ str(serializer.data["id"])
                html_message = render_to_string('acc_active_email.html', {
                'button_text': 'Verify Account',
                'button_link': activate_url
                })
               
                email_body=  strip_tags(html_message)
                mail_subject = 'Activate your Account'  
            
        
                to_email =serializer.data["email"]  
                email = EmailMultiAlternatives(  
                            mail_subject, email_body, to=[to_email]  
                )  
                email.attach_alternative(html_message, 'text/html')
                email.send()  
            
                # User.objects.filter(id=serializer.data["id"]).update(verify_email=1)         
                return Response({"Success":"response.json()","token":account_activation_token.make_token(save_obj),"id":serializer.data["id"]},status=status.HTTP_201_CREATED)
         

            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

"""API TO GET INFLUENCER PAYMENT TRANSFER DETAILS"""
class InfluencerTransfer(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            sale=FeePaid.objects.filter(influecerid=self.request.user.id,campaign_id__campaign_status=2).values("influ_amount","vendorid_id__username","influecerid_id__username","campaign_id__campaignid__campaign_name","influecerid_id__fee").order_by("-id")
           
            return Response({"code":200,"data":sale},status=status.HTTP_200_OK)
        except Exception as e:
            
            return Response({"code":400,"data":"data not found"},status=status.HTTP_400_BAD_REQUEST)
        
        
        


