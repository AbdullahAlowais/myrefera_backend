from django.shortcuts import render,HttpResponse,redirect
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from AdminApp.models import *
from StoreApp.models import *
from AdminApp.serializer import *
from rest_framework.authtoken.models import Token
from CampaignApp.models import *
from CampaignApp.serializer import *
from rest_framework.authentication import TokenAuthentication
from django.contrib import auth
from AdminApp.permission import *
from django.contrib.auth.decorators import login_required
from itertools import chain
import requests
from django.http import JsonResponse
from Affilate_Marketing.settings import API_VERSION
from django.utils.crypto import get_random_string
from AdminApp.utils import *
import stripe
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
import calendar
from InfluencerApp.utils import *
from InfluencerApp.models import *

# Create your views here.


"""FUNCTION TO GET ACCESS TOKEN"""
def access_token(request,id):
    user_obj=User.objects.filter(id=id)
    shop=user_obj.values("shopify_url")[0]["shopify_url"]
    acc_tok=Store.objects.filter(store_name=shop).values("access_token")[0]["access_token"]
   
    return acc_tok,shop
    
    
"""function to get sales report and total order count"""    
@login_required
def show(request):
    total_sales = 0 
    sales_reports1=[]
    total_order_count=0
    vendor_store=[]
    sale_val=[]
    vendor_data = User.objects.filter(user_type=3).values("shopify_url")
  
 
    for shop in vendor_data:
        get_tok = Store.objects.filter(store_name=shop["shopify_url"]).values("access_token", "store_name")

        if get_tok:
            for token in get_tok:
                headers = {"X-Shopify-Access-Token": token["access_token"]}
                store_name = token["store_name"]

                url = f"https://{store_name}/admin/api/2022-10/orders.json?status=active"
                response = requests.get(url, headers=headers)
                
                sales_data = response.json().get('orders', [])
                sales_report = 0 
                order_count=0
          
                for order in sales_data:
                    total_price = float(order['total_price'])
                    discount_codes = order.get("discount_codes", [])

                    if discount_codes:
                        sales_report += total_price
                        total_sales += total_price
                        order_count += 1  
                
                sales_reports1.append({"store_name": store_name, "sales_report": sales_report,"order_count":order_count})
    for i in sales_reports1:
        if i["sales_report"]:
            total_order_count+=i["order_count"]
            vendor_store.append(i["store_name"])
            sale_val.append(i["sales_report"])
    rouded_value=round(total_sales,2)
    return render(request,'index.html',{"total":rouded_value,"sales_report":sales_reports1,"count":total_order_count,"vendor":vendor_store,"sale_val":sale_val})


"""function to login superuser"""
def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if user.is_superuser==1:
                login(request, user)
                
                return HttpResponse("successfully")
            else:
                return HttpResponse("User is not superadmin")
        else:
            return HttpResponse("Incorrect email or password")
    elif request.user.is_anonymous:
        return render(request,'login.html')
    else:        
        return redirect("dashboard")



"""function to logout superuser"""
def logout_(request):
    auth.logout(request)

    return redirect('login1')

"""User login Api"""
class Login(APIView): 
    def post(self, request):
        username = request.data.get('email') 
        
        password = request.data.get('password')
        user = authenticate(username=username, password=password)   
        if user:
            login(request, user)
           
            refresh=Token.objects.create(user=user)
            return Response({'Success':"Login Successfully",'Token':str(refresh)}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        
"""Superuser profile update Api"""
class ProfileUpdate(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsSuperuser]
    def put(self,request,pk):
        try:
            influencer = User.objects.get(pk = pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=UpdateUserSerializer(influencer,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


        
"""Influencer api to get,create,update,delete"""
class InfluencerViewSet(viewsets.ViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsSuperuser]
    
    def list(self, request):
        infu_list=User.objects.filter(user_type =2)
        serializer = UserSerializer(infu_list,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)

    def create(self, request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_type =2)
            return Response({"Success": "Influencer Created Successfully."},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            influencer = User.objects.get(pk = pk,user_type=2)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=UpdateUserSerializer(influencer,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        influencer= User.objects.get(pk=pk,user_type=2)
        influencer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




"""Api to get Campaign list"""
class CampaignView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsSuperuser]
    def get(self,request):   
        campaign_list=Campaign.objects.all()
        serializer = CampaignSerializer(campaign_list,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)


"""List of Campaign api to get,create,update,delete"""
class CampaignViewSet(viewsets.ViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsSuperuser]
    def list(self, request):
        campaign_list=Campaign.objects.all()
        serializer = CampaignSerializer(campaign_list,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)

    def create(self, request):
        serializer=CampaignSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success":"Campaign create successfully","product_details":serializer.data},status=status.HTTP_200_OK)
        
        return Response({"error":"Campaign not created"},status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            campaign_get = Campaign.objects.get(pk = pk)
      
        except Campaign.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=UpdateCampaignSerializer(campaign_get,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        camp_del=Campaign.objects.filter(id=pk)
        camp_del.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





"""Logout api"""
class LogoutView(APIView):
    permission_classes = [IsSuperuser]
    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=204)
   
   
   

"""change password function"""
@login_required
def profile_update(request):
    user_obj=User.objects.filter(id=request.user.id).values_list("email","username")
    if user_obj:
        data=user_obj
        email=data[0][0]
        username=data[0][1]
    if request.method == "POST":
        password = request.POST.get('password')
        email = request.POST.get('email')
        username = request.POST.get('username') 
        if password:
            user_obj=User.objects.filter(id=request.user.id).update(email=email,password=make_password(password),username=username)
        else:
           
            user_obj=User.objects.filter(id=request.user.id).update(email=email,username=username)
        messages.success(request, "Profile Updated Successfuly")
        return render(request, "profileupdate.html",{"email":email,"username":username})
    return render(request, "profileupdate.html",{"email":email,"username":username})


"""Function to get campaign list"""
@login_required
def campaign_list(request):
    lst=[]
    campaign_model=Campaign.objects.filter(status=2)
   
    for i in campaign_model:
        if i.influencer_name:
            # val=ast.literal_eval(i.influencer_name)
            val=ast.literal_eval(i.influencer_name)
            z=ModashInfluencer.objects.filter(id__in=val).values_list("username",flat=True)

            lst.append(z)
    for i in lst:
        pass
    return render(request,"campaignlist.html",{"data":campaign_model,"influencer_name":lst})
    

"""Api to get marketplace list"""    
@login_required
def marketplace_list(request):
    lst=[]
    campaign_model=Campaign.objects.filter(status=1)
    return render(request,"campaignlist.html",{"data":campaign_model,"influencer_name":lst})
    
    
"""Function to get single campaign data"""    
@login_required
def Single_camp(request,id):
    single_obj=Campaign.objects.filter(id=id).values()
    product_data=Product_information.objects.filter(campaignid_id=id).values("product_name")
    
    product_name=[]
    for i in range (len(product_data)):
        product_name.append(product_data[i]["product_name"])
    vendor_name=Campaign.objects.filter(id=id).values("vendorid__username")[0]["vendorid__username"]
   
    campaign_name=single_obj[0]["campaign_name"]
    description=single_obj[0]["description"]
    offer=single_obj[0]["offer"]
    influencer_fee=single_obj[0]["influencer_fee"]
    influencer_lst=[]
    if single_obj[0]["influencer_name"]:
       
        val=ast.literal_eval(single_obj[0]["influencer_name"])
        z=ModashInfluencer.objects.filter(id__in=val).values()
       
        for i in range(len(z)):
            name=z[i]["username"]
           
            influencer_lst.append(name)
    context={"influencer_name":influencer_lst,"camapign_name":campaign_name,"vendor_name":vendor_name,"influencer_fee":influencer_fee,"description":description,"product_name":product_name,"offer":offer}
    return render(request,"singlecamp.html",context)
 
 
"""Api to get single vendor Informations""" 
@login_required
def Single_Vendor(request,id):
    
    single_obj=User.objects.filter(id=id).values()

    camp_obj=Campaign.objects.filter(vendorid_id=id,draft_status=0,status=2).values()
   
    lst1=[]
    for i in camp_obj:
        if i["influencer_name"]:
            val=ast.literal_eval(i["influencer_name"])
            z=ModashInfluencer.objects.filter(id__in=val).values()
            for k in range(len(z)):
                name=z[k]["username"]
                ids=z[k]["id"]
                
                if i["vendorid_id"]==id:
                    dict1={
                        "influencer_name":name,
                        "id":i["id"],
                        "influencer_id":ids
                    }
                    lst1.append(dict1)
                
   
    product_data1=Product_information.objects.filter(vendor_id=id,campaignid_id__draft_status=0,campaignid_id__status=2)
   
    vendor_campaign=Campaign.objects.filter(vendorid_id=id,draft_status=0,status=2)
    lst=[]
    for i in vendor_campaign:
        dict={
            "campaign_name":i.campaign_name,
            "description":i.description,
            "offer":i.offer,
            "influencer_fee":i.influencer_fee, 
            "product_name":[],
            "amount":[],
            "influencer_name":[],
            "influencer_id":[],
            "id":i.id,    
            "sale":""
        }
        lst.append(dict)
  
    vendor_campaign1=Campaign.objects.filter(vendorid_id=id,draft_status=0,status=2).values("id")
    result = list(chain(product_data1.values("product_name","campaignid","amount")))
   
    combined_data = []
    
    campaign_ids = set(item['campaignid'] for item in result)
    for campaign_id in campaign_ids:
        
        product_names = [item['product_name'] for item in result if item['campaignid'] == campaign_id]
        for item in result: 
            if item['campaignid'] == campaign_id:
                pass
        combined_data.append({'product_name': product_names,"id":campaign_id})
        
        
      
    combined_data1 = []
    
    campaign_ids1 = set(item['id'] for item in lst1)
  
    for campaign_id in campaign_ids1:
        product_names = [item['influencer_name'] for item in lst1 if item['id'] == campaign_id]      
        influencer_id = [item['influencer_id'] for item in lst1 if item['id'] == campaign_id]  
     
        combined_data1.append({'influencer_name': product_names,"id":campaign_id,"influencer_id":influencer_id})
 
    
      
    for i in combined_data1:
        for j in lst:
            if j["id"]== i["id"]:   
                j["influencer_name"]=i["influencer_name"]
                j["influencer_id"]=i["influencer_id"]
                
    
    for i in combined_data:
        for j in lst:
            if j["id"]== i["id"]:   
                j["product_name"]=i["product_name"]
                
      
    final_lst1=[] 
    campaign_obj2=VendorCampaign.objects.filter(campaign_status=2,vendor_id=id) 
                
    for i in campaign_obj2:
            dict1={
                "campaignid_id":i.campaignid.id,
                "campaign_name": i.campaignid.campaign_name,
                "influencer_name":i.influencerid.id,
                
            }
    
            final_lst1.append(dict1)
    
    

    user=User.objects.filter(id=id).values("shopify_url")
    
    get_tok=Store.objects.filter(store_name=user[0]["shopify_url"]).values("access_token")
    if get_tok:
        shopify_store = user[0]["shopify_url"]
        headers= {"X-Shopify-Access-Token": get_tok[0]["access_token"]}
        url = f'https://{shopify_store}/admin/api/2022-10/orders.json?status=any'

        

        response = requests.get(url,headers=headers)
        
        sales_by_coupon = {}

        if response.status_code == 200:
            orders1 = response.json().get('orders', [])
        
            for order in orders1:
                line_items = order.get('discount_codes', [])
            
                total_price = order.get('total_price')
                


                if line_items:
                    coupon_code = line_items[0].get('code')
                    
                
                
                    if coupon_code in sales_by_coupon:
                        sales_by_coupon[coupon_code] += float(total_price)
                        
                    else:
                        sales_by_coupon[coupon_code] = float(total_price)
                                    
                
            sale=list(sales_by_coupon.keys())
            
            amount=list(sales_by_coupon.values())
            coup_dict={}
           
            for  i in sale:    
                    check=Product_information.objects.filter(coupon_name__contains=i).values("campaignid","coupon_name")
                
                    for z in check:
                        if "coupon_name" in z:
                            list_value = eval(z["coupon_name"])
                
                            campaign_id = z["campaignid"]
                            if campaign_id in coup_dict:
                                coup_dict[campaign_id].extend(list_value)
                            else:
                                coup_dict[campaign_id] = list_value

            dict_lst = [coup_dict]
    
            sale_by_id = {}
        
            for campaign_id, coupon_names in coup_dict.items():
                sale = 0.0
                
                for coupon_name in set(coupon_names):
                    if coupon_name in sales_by_coupon:
                        sale += sales_by_coupon[coupon_name]
                sale_by_id[campaign_id] = sale
            
                campaign_name = Campaign.objects.filter(id=campaign_id).values_list('campaign_name', flat=True).first() 
                sale_by_id[campaign_id] = sale
        
            for sale in lst:
                sale_id = sale['id']
                sale_value = sale_by_id.get(sale_id, 0)
                sale_by_id[sale_id] = sale_value
                sale['sale'] = round(sale_value,2)
            
          
          
            return render(request,"campaignlist.html",{"vendor":vendor_campaign,"vendor_campaign":lst,"product_data":combined_data,"single_vendor":single_obj,"final_list":final_lst1})
        return render(request,"campaignlist.html",{"vendor":vendor_campaign,"vendor_campaign":lst,"product_data":combined_data,"single_vendor":single_obj,"final_list":final_lst1})
    return render(request,"campaignlist.html")



"""function to get all vendor lists"""
@login_required
def vendor_list(request):
    vendor_data=User.objects.filter(user_type=3)
    return render(request,"vendorlist.html",{"vendor":vendor_data})
   
   
"""function to change vendor status"""
def change_status(request):
    if request.method == "GET":
        value=request.GET.get("status")
      
      
        ids=value[1:]
       
        if value[0]=="a":
            
            User.objects.filter(id=int(ids)).update(vendor_status=True)
            return HttpResponse("User is Active")
        else:
          
            User.objects.filter(id=int(ids)).update(vendor_status=0)
            return HttpResponse("User is Deactivated")
       
       
"""Function to get sale data and order list"""
def Order_list(request,id):
    user=User.objects.filter(id=id).values("shopify_url")
   
    get_tok=Store.objects.filter(store_name=user[0]["shopify_url"]).values("access_token")
    if get_tok:
        shopify_store = user[0]["shopify_url"]
        headers= {"X-Shopify-Access-Token": get_tok[0]["access_token"]}

        
        url = f"https://{shopify_store}/admin/api/2023-04/orders.json?status=active"

        response = requests.get(url, headers=headers)


        
        if response.status_code == 200:
            
            
            orders3 = response.json().get("orders", [])
            product_sales = {}
         
            keys=list(product_sales.keys())
            values=list(product_sales.values())
            
            
            order_count = {str(i): 0 for i in range(1, 13)}
            orders = response.json().get("orders", [])

            for order in orders:
                created_at = order.get("created_at")
                month = int(created_at.split("-")[1])
                discount_codes = order.get("discount_codes", [])
                
                if discount_codes:
                    order_count[str(month)] += 1
            

                
            data = []
            for month in range(1, 13):
                month_name = calendar.month_name[month]
            
                count = order_count[str(month)]
                data.append({"month": month_name, "count": count})
        
        
        
            order_list=list(order_count.values())
            sales_data = response.json()['orders']
            sales_report = {}

            for month_number in range(1, 13):
                month_name = calendar.month_name[month_number]
                sales_report[month_name] = 0


            for order in sales_data:
                created_at = order['created_at']
                month_number = int(created_at.split('-')[1])
                month_name = calendar.month_name[month_number]
                total_price = float(order['total_price'])
                discount_codes = order.get("discount_codes", [])

                if discount_codes:
                    sales_report[month_name] += total_price

            sales = list(sales_report.values())
        
            return render(request,"chart.html",{'sales_data': sales,"order":order_list})
        else:
            return render(request,"chart.html")
    return render(request,"chart.html")
    


"""To get all influencer list"""
@login_required
def Influencer_list(request):
    
    Influencer=ModashInfluencer.objects.filter().values("id","username","follower","image","engagements","engagement_rate","fullname","isverified","influencerid_id__commission","admin_approved","paid_status","influencerid_id__id")

    return render(request,"Influencerlist.html",{"influencer":Influencer})


"""To get influencer based on campaign status"""
def influencer_name(request):
    if request.method == "GET":
        value=request.GET.get("status")
        
       
        camp_obj=Campaign.objects.filter(id=value,draft_status=0,status=2).values()
       
        lst1=[]
        for i in camp_obj:
          
            if i["influencer_name"]:
               
                val=ast.literal_eval(i["influencer_name"])
                z=ModashInfluencer.objects.filter(id__in=val).values()

                for k in range(len(z)):
                    
                    name=z[k]["username"]
                    ids=z[k]["id"]
                  
                    if i["id"]==int(value):
                        dict1={
                            "influencer_name":name,
                            "id":i["id"],
                            "influencer_id":ids,
                            "status":"Pending",
                        }
                        lst1.append(dict1)
        
        campaign_obj2=VendorCampaign.objects.filter(campaign_status=2,campaignid_id=value) 
        lst2=[]
        for k in lst1:
           
            for j in campaign_obj2:
           
                if k["influencer_id"] == j.influencerid.id:
                    k["status"]="Accepted"

        campaign_obj3=VendorCampaign.objects.filter(campaign_status=4,campaignid_id=value) 
        for k in lst1:
           
            for j in campaign_obj3:
           
                if k["influencer_id"] == j.influencerid.id:
                    k["status"]="Declined"

        return JsonResponse({"val":lst1})
    

"""To get campaign product"""
def product_name(request):
    if request.method == "GET":
        value=request.GET.get("status")
        product_list=[]
        product_data1=Product_information.objects.filter(campaignid_id=value,campaignid_id__draft_status=0,campaignid_id__status=2)
        for i in product_data1:
            pro_dict={ 
                      "product_name":i.product_name,
                      "coupon":i.coupon_name,
                      "amount":i.amount
                }
            product_list.append(pro_dict)
            
        return JsonResponse({"val":product_list})
    
    
    
"""forgot password to email link"""
def forgot_password(request):    
    if request.method=='POST':
        email=request.POST.get('email')
        if not User.objects.filter(email=email,is_superuser=1).first():
            return HttpResponse("1")
        token=get_random_string(length=6, allowed_chars='0123456789')
        request.session['token'] = token
        send_forget_password_mail(email,token)    
        return HttpResponse("2")
    return render(request, "forgetpassword.html")


"""forgot password to email link"""
def change_password_link(request,email,token):  
    token2 = request.session['token']
    
    if request.method == "POST":
        password = request.POST.get('password')
        conpassword = request.POST.get('conpassword')
        if int(token) == int(token2):
            if password == conpassword:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                request.session['token']=0
                msg="password changed successfully"
                return render(request, "login.html", {'msg':msg})
            msg="Your password and confirmation password do not match."   
            return render(request, "changepassword.html", {'msg':msg})
        
        return HttpResponse("invalid link")
    return render(request, "changepassword.html")
    
           
    
"""stripe payment gateway"""    
@login_required
def split_payment(request):
   
    if request.method == "POST":
        amount =1000
       
        recipient1_amount = int(amount * 0.7)
        recipient2_amount = int(amount * 0.3)  

              
        stripe.api_key = settings.STRIPE_API_KEY


        payment_method=stripe.PaymentMethod.create(
        type="card",
        card={
            "number": "4242424242424242",
            "exp_month": 8,
            "exp_year": 2024,
            "cvc": "314",
        },
        
        
        )
   
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            payment_method_types=['card'],
            payment_method=payment_method["id"],
           
        )
        
        confim=stripe.PaymentIntent.confirm(
        intent["id"],
        payment_method="pm_card_visa",
        )
      
      
        if intent.status == 'requires_payment_method':
            return render(request, 'payment_failure.html')

        if confim.status == 'succeeded':
           
            transfer1 = stripe.Transfer.create(
                amount=recipient1_amount,
                currency='usd',
                destination='acct_1N663eGaS3CgF946',
                transfer_group=intent.id,
            )

            transfer2 = stripe.Transfer.create(
                amount=recipient2_amount,
                currency='usd',
                destination='acct_1N65yo2eF54Yl928',
                transfer_group=intent.id,
            )     
            return render(request, 'payment_success.html')
    return render(request, 'payment_success.html',{"STRIPE_PUBLISHABLE_KEY":settings.STRIPE_PUBLISHABLE_KEY})



"""To create vendor account on stripe"""
@login_required
def stripe_data(request):
    
    if request.method=="POST":
        vendorids=request.POST.get("vendorids")
        secret=VendorStripeDetails.objects.filter(vendor=vendorids).values("secret_key")
        if secret:
            secret=secret[0]["secret_key"]
        match=stripe_details.objects.filter(vendor=vendorids).exists()
        if match == True:
            messages.error(request,"Account Already Exists") 
            return redirect("stripe")
        try:
            acc_data=createaccount(secret)
            stripe_det=stripe_details()
            stripe_det.vendor_id=vendorids
            stripe_det.user_id=request.user.id
            stripe_det.account_id=acc_data["id"]
            stripe_det.save()
        except stripe.error.StripeError as e:
            messages.success(request,e.user_message) 
            return render(request,"stripe.html")

        messages.success(request, "Account Created Successfully")
        return redirect("stripe")

        
        # stripe_obj=stripe_details()
        # publish_key=request.POST.get("publish")
        # secret_key=request.POST.get("secret")
        
        # stripe_obj.user_id=request.user.id
        # stripe_obj.publishable_key=publish_key
        # stripe_obj.secret_key=secret_key
        
        # if  stripe_details.objects.filter(user_id=request.user.id).exists():
        #     stripe_details.objects.filter(user_id=request.user.id).update(publishable_key=publish_key,secret_key=secret_key)
        # else:
        #     stripe_obj.save()
        # stripe_get=stripe_details.objects.filter(user_id=request.user.id).values("publishable_key","secret_key")
        
        # return render(request,"stripe.html",{"publish":stripe_get[0]["publishable_key"],"secret":stripe_get[0]["secret_key"]})
    vendor_list=VendorStripeDetails.objects.all().values("vendor__username","vendor")
   
    # stripe_get=stripe_details.objects.filter(user_id=request.user.id).values("publishable_key","secret_key")  
    # if stripe_get:
    return render(request,"stripe.html",{"data":vendor_list})
    # else:
    #     return render(request,"stripe.html")


"""To update admin commission in admin pannel"""
def charge_commission(request):
    admin_commision=commission_charges()
    if request.method=="POST":
        admin_comm=request.POST.get("commission")
        admin_commision.commission=admin_comm
        admin_commision.user_id=request.user.id
        if  commission_charges.objects.filter(user_id=request.user.id).exists():
            commission_charges.objects.filter(user_id=request.user.id).update(commission=admin_comm)
        else:
            admin_commision.save()
        commission_get=commission_charges.objects.filter(user_id=request.user.id).values("commission")  

        messages.success(request, "Commission set Successfully" )
        
        return render(request,"commission.html",{"commission":commission_get[0]["commission"]})
    commission_get=commission_charges.objects.filter(user_id=request.user.id).values("commission")  
    if commission_get:
        return render(request,"commission.html",{"commission":commission_get[0]["commission"]})

    return render(request,"commission.html")
        





# def get_coupon_codes(request):
#     user=User.objects.filter(id=22).values("shopify_url")
    
#     get_tok=Store.objects.filter(store_name=user[0]["shopify_url"]).values("access_token")
    
#     shopify_store = user[0]["shopify_url"]
#     headers= {"X-Shopify-Access-Token": get_tok[0]["access_token"]}
#     url = f'https://{shopify_store}/admin/api/{API_VERSION}/price_rules.json?status=active'
#     discount_list=[]
#     orders=[]
#     # response = requests.get(url, headers=headers)
#     # if response.status_code == 200:
#     #     price_rules = response.json().get('price_rules', [])
#     #   
#     #     for rule in price_rules:
#     #         price_rule_id = rule['id']
#     #         discount_codes_url = f"https://{shopify_store}/admin/api/{API_VERSION}/price_rules/{price_rule_id}/discount_codes.json"
#     #         discount_codes_response = requests.get(discount_codes_url, headers=headers)
           
#     #         if discount_codes_response.status_code == 200:
                
#     #             discount_codes = discount_codes_response.json().get('discount_codes', [])
#     #             for code in discount_codes:
#     #                 discount_code = code['code']
#     #                 discount_list.append(discount_code)
         
         
#     url = f'https://{shopify_store}/admin/api/{API_VERSION}/orders.json?status=active'


#     response = requests.get(url,headers=headers)
    
#     sales_by_coupon = {}

#     if response.status_code == 200:
#         orders1 = response.json().get('orders', [])
        
        
#         for order in orders1:
#             line_items = order.get('discount_codes', [])
#             line_items3 = order.get('id', [])
#             total_price = order.get('total_price')
            


#             if line_items:
#                 coupon_code = line_items[0].get('code')
#                 id = line_items3
#                 sales_by_coupon["id"]=id
            
#                 if coupon_code in sales_by_coupon:
#                     sales_by_coupon[coupon_code] += float(total_price)
                    
#                 else:
#                     sales_by_coupon[coupon_code] = float(total_price)
                            
                
#         sale=list(sales_by_coupon.keys())
#         amount=list(sales_by_coupon.values())
#         coup_dict={}
#         for  i in sale:    
#                 check=Product_information.objects.filter(coupon_name__contains=i).values("campaignid","coupon_name")
                
#                 for z in check:
#                     if "coupon_name" in z:
#                         list_value = eval(z["coupon_name"])
            
#                         campaign_id = z["campaignid"]
#                         if campaign_id in coup_dict:
#                             coup_dict[campaign_id].extend(list_value)
#                         else:
#                             coup_dict[campaign_id] = list_value

#         dict_lst = [coup_dict]
        
#         sale_by_id = {}

#         for campaign_id, coupon_names in coup_dict.items():
#             sale = 0.0
            
#             for coupon_name in set(coupon_names):
#                 if coupon_name in sales_by_coupon:
#                     sale += sales_by_coupon[coupon_name]
#             sale_by_id[campaign_id] = sale

#             campaign_name = Campaign.objects.filter(id=campaign_id).values_list('campaign_name', flat=True).first() 
#             sale_by_id[campaign_id] = [sale, campaign_name]
#         ("ordersssss",orders)           
#         return HttpResponse(orders)
#     else:
#         return HttpResponse("error")
    
    
# def influenceraccept(request,id):
#     ModashInfluencer.objects.filter(id=id).update(admin_approved=1)
#     Influencer=ModashInfluencer.objects.filter().values()

#     messages.success(request,"Influener accepted")
#     return render(request,"Influencerlist.html",{"influencer":Influencer})
    
    
# def influencerdecline(request,id):
#     ModashInfluencer.objects.filter(id=id).update(admin_approved=0)
#     Influencer=ModashInfluencer.objects.filter().values()

#     messages.error(request,"Influencer declined")
#     return render(request,"Influencerlist.html",{"influencer":Influencer})



"""Admin design to accept or reject influencer"""
def admin_decision(request):
    if request.method == "GET":
        value=request.GET.get("status")
        
        ids=value[1:]
       
        if value[0]=="a":
            
            ModashInfluencer.objects.filter(id=int(ids)).update(admin_approved=1)
            return HttpResponse("Influencer accepted")
        else:
          
            ModashInfluencer.objects.filter(id=int(ids)).update(admin_approved=0)
            return HttpResponse("Influencer Rejected")


"""To get vendor total sale"""
@login_required
def total_sales(request):
    vendor_data=User.objects.filter(user_type=3).values("shopify_url")
    for shop in vendor_data["shopify_url"]:
        get_tok=Store.objects.filter(store_name=shop).values("access_token")
        
    if get_tok:
        for token in get_tok["access_token"]:
            headers= {"X-Shopify-Access-Token":token}

        url = f"https://{shop}/admin/api/{API_VERSION}/shopify_payments/balance.json"
        response = requests.get(url, headers=headers)
       
    return render(request,"dashboard.html")


"""Influencer fee paid status"""
@login_required
def paymentdetails(request):
    try:
        paymentdata=FeePaid.objects.filter(campaign_id_id__campaign_status=4)
        modash_data=ModashInfluencer.objects.all()
      

        return render(request,"influencerpaid.html",{"paymentdata":paymentdata,"modash_data":modash_data})
    except Exception as e:
        
        return render(request,"influencerpaid.html")


"""To refund money """
@login_required
def Refundmoney(request):
    try:
        if request.method == "POST":
            charge=request.POST.get("charge")
            id = request.POST.get("id")
            amount = request.POST.get("amount")
            paid=refund_money(request,charge,amount)
            FeePaid.objects.filter(id=id).update(status=1)
            
            return HttpResponse("paid")
    except Exception as e:
        return HttpResponse("fail")
  

"""Influencer fee status paid or not"""
@login_required
def Influncerpaid(request):
    try:
        if request.method == "POST":
            amount_paid = request.POST.get("amount_paid")
            if amount_paid == "":
                return HttpResponse("empty")
            
            id = request.POST.get("id")
            infl_amount = FeePaid.objects.get(id=id).amount
            previous_amount = FeePaid.objects.get(id=id).influ_amount
            
            if int(previous_amount) == int(infl_amount):
                return HttpResponse("already")
            
            if int(amount_paid) + int(previous_amount) > infl_amount:
                return HttpResponse("failed")

                  
            if int(infl_amount)<int(amount_paid):
               
                return HttpResponse("failed")
            totat_amount = int(amount_paid) + int(previous_amount)            
            FeePaid.objects.filter(id=id).update(influ_amount=totat_amount)
            return HttpResponse("done")
        
        paymentdata=FeePaid.objects.filter(campaign_id_id__campaignid__status=2).order_by("-id").values('id','charge_id','amount','campaign_id__campaign_status','campaign_id__campaignid__campaign_name','influ_amount','vendorid__username','influecerid_id')

        
        data = []

        for i in paymentdata:
            try:
                modash_data=ModashInfluencer.objects.filter(influencerid = i['influecerid_id']).values('username').first()
                i['username'] = modash_data['username']
            except Exception as e:
                i['username'] = ""

            data.append(i)

        adminfees=commission_charges.objects.values("commission")
        
      
        # return render(request,"paid.html",{"paymentdata":paymentdata,"modash_data":modash_data})
        return render(request,"paid.html",{"paymentdata":data})
    except Exception as e:

        return render(request,"paid.html")
    
        
    
"""Total fee paid"""
@login_required
def TotalPayment(request): 
    balance_data=balance()

    return render(request,"totalpayment.html",{"commission":balance_data[0]["adminfee__sum"],"amount_transfer":balance_data[1]["influ_amount__sum"],"total_earn":balance_data[2]["amount__sum"]})


"""Market influencer fee status paid or not"""
@login_required
def MarketInfluncerpaid(request):
    try:
        if request.method == "POST":
            amount_paid = request.POST.get("amount_paid")
            if amount_paid == "":
                return HttpResponse("empty")
            
            id = request.POST.get("id")
            infl_amount = FeePaid.objects.get(id=id).amount
            previous_amount = FeePaid.objects.get(id=id).influ_amount
            
            if int(previous_amount) == int(infl_amount):
                return HttpResponse("already")
            
            if int(amount_paid) + int(previous_amount) > infl_amount:
                return HttpResponse("failed")

                  
            if int(infl_amount)<int(amount_paid):
               
                return HttpResponse("failed")
            totat_amount = int(amount_paid) + int(previous_amount)            
            FeePaid.objects.filter(id=id).update(influ_amount=totat_amount)
            return HttpResponse("done")
        
        paymentdata=FeePaid.objects.filter(campaign_id_id__campaignid__status=1).order_by("-id")
        modash_data=ModashInfluencer.objects.all()
        adminfees=commission_charges.objects.values("commission")
        return render(request,"marketpaid.html",{"paymentdata":paymentdata,"modash_data":modash_data})
    except Exception as e:

        return render(request,"marketpaid.html")
    

"""To update commission in user table"""    
@login_required
def UpdateCommission(request):
    try:
        if request.method == "POST":
            commission = request.POST.get("commission")

            if commission == "":
                return HttpResponse("empty")
            
            id = request.POST.get("id")

            upd_commission=User.objects.filter(id=id).update(commission=commission)
            return HttpResponse("commission earned")
    except Exception as e:
        return render(request,"marketpaid.html")

            

