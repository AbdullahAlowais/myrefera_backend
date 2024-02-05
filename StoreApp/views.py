from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect,render
from Affilate_Marketing.settings import SHOPIFY_API_KEY,SHOPIFY_API_SECRET,app_name,redirect_url,shopify_scopes
import requests
import hmac
import hashlib
import json
from StoreApp.models import *
from AdminApp.models import *
from rest_framework import status
import string
import random
from urllib.parse import urlencode
from django.http import HttpResponseRedirect
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from Affilate_Marketing.settings import SHOPIFY_API_KEY,SHOPIFY_API_SECRET,API_VERSION

# Create your views here.


"""API TO INSTALL APP"""
class InstallView(APIView):
    def get(self, request):
        shop = request.GET.get('shop')  
        if not shop:
                return Response({'error': 'Missing shop parameter'}, status=400)
        else:    
            shop2=Store.objects.filter(store_name=shop)
            if shop2:      
                    return redirect(f"https://myrefera.com/frontend/#/dashboard?shop="+shop,{'dashboard_url':f'https://admin.shopify.com/store/marketplacee-app/apps/{app_name}?shop='+ shop})
            else:
                redirect_uri=redirect_url
              #  scopes =['read_orders','write_products','read_themes','write_themes','read_customers','write_customers','read_files','write_files','write_price_rules','read_reports','write_reports','read_shopify_payments_payouts']
                scopes = [
    'read_orders', 'write_products', 'read_themes', 'write_themes',
    'read_customers', 'write_customers', 'read_files', 'write_files',
    'write_price_rules', 'read_reports', 'write_reports',
    'read_shopify_payments_payouts']
                get_shop=Store.objects.filter(store_name=shop)
                # if get_shop:
                #     return redirect(f"https://admin.shopify.com/store/marketplacee-app/apps/{app_name}")
                auth_url = f"https://{shop}/admin/oauth/authorize?client_id={SHOPIFY_API_KEY}&scope={'+'.join(scopes)}&redirect_uri={redirect_uri}" 
                return Response({"url":auth_url},status=status.HTTP_200_OK)   



#AUTHORIZE APP URL
"""API TO AUTHORIZE APP URL"""
class CallbackView(APIView):
    def get(self, request):
        shop = request.query_params.get('shop')
        code = request.query_params.get('code')
        hmac_digest = request.query_params.get('hmac')    
        params=request.GET
        sorted_params='&'.join([f"{key}={params[key]}" for key in sorted(params)])
        secret = bytes(SHOPIFY_API_SECRET, 'utf-8')
        hmac_calculated = hmac.new(secret, sorted_params.encode('utf-8'), hashlib.sha256).hexdigest()
        if not(request.GET,hmac_calculated):
            return Response({'error': 'Invalid HMAC'})
      
        access_token = self.get_access_token(shop,code,hmac_calculated)
        
        
        result=dict(json.loads(access_token.text))
  
        acc_tok=result["access_token"]
        shop_details=self.details(shop,acc_tok)
 
        shop_name=shop.split(".")[0]
        return redirect(f"https://admin.shopify.com/store/{shop_name}/apps/marketplace-54?shop="+shop)
        # return Response({"success":"app_created","shop_url":f"https://admin.shopify.com/store/{shop_name}/apps/marketplace-49?shop="+shop})


    def get_access_token(self,shop,code,hmac_calculated):
       
        url = f"https://{shop}/admin/oauth/access_token"
        redirect_uri="https://api.myrefera.com/store/callback/"
     
        payload = {
            "client_id": SHOPIFY_API_KEY,   
            "client_secret": SHOPIFY_API_SECRET,
            "code": code,
            "redirect_uri":redirect_uri
        }
        
        response = requests.post(url, json=payload)
        
        result=dict(json.loads(response.text))
         

        store_obj=Store()
        store_obj.store_name=shop
        store_obj.token=hmac_calculated
        store_obj.code=code
        #store_obj.userid=self.request.user.id
        store_obj.access_token=result["access_token"]  
           
        store_obj.save()                            
        return response
    
    def details(self,shop,acc_tok):
        
        shop_url = f"https://{shop}/admin/api/{API_VERSION}/shop.json"
        headers = {'X-Shopify-Access-Token': acc_tok}
        response = requests.get(shop_url, headers=headers)
        if response.status_code == 200:
                
                shop_data = response.json()['shop']
                shop_name = shop_data['name']       
                shop_email = shop_data['email']
                return response
        # return Response({"error":"details"})

"""API TO GET SHOP DETAILS"""
class StoreDetails(APIView):
    def post(self,request):
        shop_url = f"https:///admin/api/{API_VERSION}/shop.json"
        headers = {'X-Shopify-Access-Token': "shpua_a9e28531b1ea7a90f730438666c922ef"}
        response = requests.get(shop_url, headers=headers)
        if response.status_code == 200:
            
                shop_data = response.json()['shop']
                shop_name = shop_data['name']
                return Response({"success":"details"})
        return Response({"error":"details"})
    
    
    
 
# class WebhookHandler(APIView):
#     authentication_classes=[TokenAuthentication]
#     permission_classes = [IsAuthenticated]  
#     def post(self, request,):
#         user_obj=User.objects.filter(id=self.request.user.id)
#         shop=user_obj.values("shopify_url")[0]["shopify_url"]
#         acc_tok=Store.objects.filter(store_name=shop).values("access_token")[0]["access_token"]
#         shopify_domain = 
#         webhook_url = 'https://api.myrefera/webhook-handler'
#         topic = 'orders/create'
#         access_token = get_shopify_access_token()
#         register_webhook(shopify_domain, webhook_url, topic, access_token)
#         return Response({'message': 'Webhook registered successfully'})

# def get_shopify_access_token():
#     # Get the access token for your Shopify app
#     # You can obtain this by following the OAuth authentication flow in your app
#     access_token = 'your-app-access-token'
#     return access_token

# def register_webhook(shopify_domain, webhook_url, topic, access_token):
#     # Register a new webhook for the specified topic and URL
#     webhook_endpoint = f'https://{shopify_domain}/admin/api/2021-07/webhooks.json'
#     webhook_headers = {
#         'Content-Type': 'application/json',
#         'X-Shopify-Access-Token': access_token
#     }
#     webhook_payload = {
#         'webhook': {
#             'topic': topic,
#             'address': webhook_url,
#             'format': 'json'
#         }
#     }
#     response = requests.post(webhook_endpoint, headers=webhook_headers, json=webhook_payload)

#     # Check if the webhook was registered successfully
#     if response.status_code == 201:
#     else:
        
        
    
"""API TO CHECK STORE"""    
class CheckStore(APIView):
    
    def get(self,request):
        input_url = "marketplacee-app.myshopify.com"
        shop=f"https://{input_url}/admin/api/{API_VERSION}/shop.json"
        response = requests.get(f"https://{input_url}/admin/api/{API_VERSION}/shop.json")
        
        return response.status_code == 200


                    

       
    