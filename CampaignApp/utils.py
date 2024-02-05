from CampaignApp.models import *
from StoreApp.models import *
from rest_framework.response import Response
import ast
from ShopifyApp.models import *
from CampaignApp.views import *
from Affilate_Marketing.settings import SHOPIFY_API_KEY,SHOPIFY_API_SECRET,API_VERSION
import requests
import stripe
from django.core.mail import EmailMessage 
from django.contrib.auth import get_user_model



def product_details(self,request,val_lst,req_id):  
    for i in range(len(val_lst)):
            product=Product_information()
            product.vendor_id=self.request.user.id
            product.campaignid_id=req_id.id
            product.product_name=val_lst[i]["product_name"]
            # product.product_id=val_lst[i]["product_id"]
            product.coupon_name=val_lst[i]["coupon_name"]
            product.coupon_id=val_lst[i]["coupon_id"]
            product.amount=val_lst[i]["amount"]
            product.discount_type=val_lst[i]["discout_type"]
            product.save()
     
       
                    
def product_name(self,request,req_id,arg,arg_id):
    for i in  range(len(arg)):
        product=Product_information()
        product.vendor_id=self.request.user.id
        product.campaignid_id=req_id.id
        product.product_name=arg[i]
        product.product_id=arg_id[i]
        product.save()


def influencer_details(self,request,int_list,req_id):
    for i in int_list:
            vendor_obj=VendorCampaign()
            vendor_obj.influencerid_id=i
            vendor_obj.campaignid_id=req_id.id
            vendor_obj.vendor_id=self.request.user.id
            vendor_obj.save()    
     
            last_user=FeePaid.objects.filter(vendorid=self.request.user.id).last() 
            # print("last_user", last_user) 
            # print("id",self.request.user.id)
            # try:
            #     i_fee_id =  VendorCampaign.objects.filter(influencerid=i).values('influencerid__influencerid__fee','influencerid__influencerid__id')
            #     i_fee = i_fee_id[0]['influencerid__influencerid__fee']
            #     i_id = i_fee_id[0]['influencerid__influencerid__id']
            # except Exception as e:
            #     i_fee = None
            #     i_id = None
           
            # last_user = FeePaid()
            last_user.vendorid_id = self.request.user.id
            last_user.campaign_id_id = vendor_obj.id
            # last_user.influecerid_id = i_id
            # last_user.amount = int(i_fee)

            last_user.save()
                     
            data=ModashInfluencer.objects.filter(influencerid=i)

            ModashInfluencer.objects.filter(id=i).update(paid_status=0)


            notification_obj=Notification()
            notification_obj.influencerid_id=i
            notification_obj.send_notification=1
            notification_obj.vendor_id=self.request.user.id
            notification_obj.campaignid_id=req_id.id
            notification_obj.save()
            
            
            
def coupon_check(self,request,val_lst2,cup_lst,coup_lst):
    val_lst2=(request.data["product_discount"])
    coup_lst=[]
    cup_lst=[]
    dict1={}
    if val_lst2:
        for i in  range (len(val_lst2)):
            for j in val_lst2[i]["coupon_name"]: 
                match_data=Product_information.objects.filter(coupon_name__contains=j,vendor_id=self.request.user.id)
                for i in match_data:
                    if j in ast.literal_eval(i.coupon_name):
            
                        
                        data_check=True
                    else:
                        data_check=False     
                
                    if data_check == True:
                        cup_lst.append(j)
                        dict1={str(cup_lst):data_check}
                        
                        
                        cup_lst.append(dict1)
                        coup_lst.append(data_check)
                        

                    if True in coup_lst:
                        cop=(list(dict1.keys())[0])
                    
                        cop_lst=ast.literal_eval(cop)
    
    
                
                        return cop
                
                        
                




def access_token(self,request):
    user_obj=User.objects.filter(id=self.request.user.id)
    shop=user_obj.values("shopify_url")[0]["shopify_url"]
    acc_tok=Store.objects.get(store_name=shop).access_token

    return acc_tok,shop


def ExpiryCoupondelete(self,request):
    
    acc_tok=access_token(self,request)
    
    headers= {"X-Shopify-Access-Token": acc_tok[0]}
    price_rule=request.query_params.get('price')
    product_info=Product_information.objects.filter(campaignid_id__campaign_exp=0,vendor_id=self.request.user.id).values_list("coupon_name",flat=True)
    product_info2=Product_information.objects.filter(campaignid_id__campaign_exp=0,vendor_id=self.request.user.id).values_list("coupon_id",flat=True)

    
    
    for coupon in product_info2:
        
        if coupon:
            str_lst=ast.literal_eval(coupon)
           
            cop_id=influencer_coupon.objects.filter(coupon_id__in=str_lst,vendor=self.request.user.id).values_list("coupon_id",flat=True)

            if cop_id:
                url =f'https://{SHOPIFY_API_KEY}:{SHOPIFY_API_SECRET}@{acc_tok[1]}/admin/api/{API_VERSION}/price_rules/{cop_id[0]}.json'
        
        
                response = requests.delete(url,headers=headers)

                delete_coup=influencer_coupon.objects.filter(coupon_name__in=str_lst,vendor=self.request.user.id).delete()
    return "DONE"


def checkout(self,request,plan):

    session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                            {
                                'price': plan,
                                'quantity': 1,
                            },
                        ],
                    mode='subscription',
                    success_url='https://myrefera.com/frontend/#/thankyou?shop=marketplacee-app.myshopify.com',
                    cancel_url='https://myrefera.com/payment-failed',
                    billing_address_collection='auto'
    )

    return session          



def success(self,request,subscription_id,price_id,start_date,end_date,amount):
    subscription=StripeSubscription()
    subscription.vendor_id=self.request.user.id
    subscription.status=1
    subscription.subscription_id=subscription_id
    subscription.price_id=price_id
    subscription.start_date=start_date
    subscription.end_date=end_date
    subscription.amount=amount
    subscription.save()
    
    credit=CampaignCredit()
    if amount == 100:
        credit.total_campaign=10
    elif amount == 250:
        credit.total_campaign=30
    else:
        credit.total_campaign=50
        
    credit.status=1
    credit.vendor_id=self.request.user.id
    credit.start_date=start_date
    credit.end_date=end_date
    
    return "Created"


    
def customer(request):
       
        value=User.objects.get(id=request.user.id)
        customer_data=stripe.Customer.create(name=value.username, email=value.email)
       
        stripe_customer_id = customer_data['id']     
        return customer_data
    
 
    
def method(request,customerdata):
    
    value=User.objects.get(id=request.user.id)
    #if value.customer_id and value.card_number:
        #return "Already Exists"
    card_number=request .data.get("card")
    expiry_month=request.data.get("exp_month")
    expiry_year=request.data.get("expiry_year")
    csv=request.data.get("cvc")

    
    
    payment_method=stripe.PaymentIntent.create(
        amount=2000,    
        currency="aed",
        automatic_payment_methods={"enabled": True},
        )

    payment=payment_method["id"]

    
    attach_payment=stripe.PaymentMethod.attach(
            payment, 
            customer=customerdata,
        )
   
    
    return payment_method
    
    


def confirm(request,customerdata,influencer_id_fee):

    if influencer_id_fee == None:
        influencer_id_fee = 0

    added_fee=int(influencer_id_fee)*10/100

    intent = stripe.PaymentIntent.create(
    amount=int(influencer_id_fee+added_fee),
    customer=customerdata,
    currency='aed',
    payment_method_types=['card'],
    )       
   

    confirm=stripe.PaymentIntent.confirm(
    intent["id"],
    payment_method="pm_card_visa",
    )  
    # if confirm.status == 200:


    return confirm



def register(request,serializer):
   
    serializer.save(user_type=3)
    mail_subject = 'Vendor Register'  
    email_body= "HI"  +  " "  +  serializer.data["username"] + " " + "your Shop Register Successfully"

    to_email =serializer.data["email"]  
    email = EmailMessage(  
                mail_subject, email_body, to=[to_email]  
    )  
    email.send()  
    return "Successfully Registered"
    
    

    