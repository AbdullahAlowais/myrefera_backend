from AdminApp.models import User
from StoreApp.models import Store
import requests
from Affilate_Marketing.settings import base_url ,headers ,SHOPIFY_API_KEY,SHOPIFY_API_SECRET,API_VERSION
from rest_framework.response import Response
from rest_framework import status


def access_token(self,request):
    user_obj=User.objects.filter(id=self.request.user.id)
    shop=user_obj.values("shopify_url")[0]["shopify_url"]
    acc_tok=Store.objects.filter(store_name=shop).values("access_token")[0]["access_token"]
   
    return acc_tok,shop


def one_time_discount(price_id,shop,headers,discount):
    
        discount_code_endpoint = f'https://{SHOPIFY_API_KEY}:{SHOPIFY_API_SECRET}@{shop}/admin/api/{API_VERSION}/price_rules/{price_id}/discount_codes.json'

        discount_code_data = {
            'discount_code': {
                'code': discount,
                'usage_limit': None,
                'customer_selection': 'all',
                "once_per_customer": True, 
                'starts_at': '2023-04-06T00:00:00Z',
                'ends_at': '2023-04-30T23:59:59Z'
            }
        }


        discount_code_response = requests.post(discount_code_endpoint, json=discount_code_data,headers=headers)
    
        if discount_code_response.status_code == 201:
            return discount_code_response
        else:
    
            pp=delete_price_rule(price_id,shop, headers)
            return discount_code_response
        
        
def delete_price_rule(price_rule_id, shop, headers):
   
    
    delete_url = f'https://{shop}/admin/api/{API_VERSION}/price_rules/{price_rule_id}.json'
    response = requests.delete(delete_url, headers=headers)

    if response.status_code == 200:
        return True  # Price rule deleted successfully
    else:
        return False  # Failed to delete price rule
    
    
    
#API for particular product
def discount_code1(price_id,shop,headers,discount_code):
    
    
    discount_code_endpoint = f'https://{SHOPIFY_API_KEY}:{SHOPIFY_API_SECRET}@{shop}/admin/api/{API_VERSION}/price_rules/{price_id}/discount_codes.json'

    # Set up the data for the discount code
    discount_code_data = {
        'discount_code': {
            'code': discount_code,
            'usage_limit': None,
            'customer_selection': 'all',
            "once_per_customer": True, 
            'starts_at': '2023-04-06T00:00:00Z',
            'ends_at': '2023-04-30T23:59:59Z',
            

        }
    }


    discount_code_response = requests.post(discount_code_endpoint, json=discount_code_data,headers=headers)
    
    if discount_code_response.status_code == 201:
        return discount_code_response
    else:
    
        pp=delete_price_rule(price_id,shop, headers)
        return discount_code_response
      
      
def discount_code5(price_rule,shop,headers,discount_code):
    discount_code_endpoint = f'https://{SHOPIFY_API_KEY}:{SHOPIFY_API_SECRET}@{shop}/admin/api/{API_VERSION}/price_rules/{price_rule}/discount_codes.json'
    get_response = requests.get(discount_code_endpoint, headers=headers)
    discount_code_id=get_response.json()["discount_codes"][0]['id']

    patch_url = f"https://{shop}/admin/api/2021-10/price_rules/{price_rule}/discount_codes/{discount_code_id}.json"
    

    data = {
    "discount_code": {
        "id": discount_code_id,
        "code": discount_code,
      
    }
}
    discount_code_response = requests.patch(patch_url, json=data,headers=headers)

    if discount_code_response.status_code == 200:
        return Response({"success":discount_code_response.json()},status=status.HTTP_200_OK)
    else:
        return Response({"error":discount_code_response.json()},status=status.HTTP_400_BAD_REQUEST)
        
        
        
def discount_code9(price_rule,shop,headers,discount_code):
    
    discount_code_endpoint = f'https://{SHOPIFY_API_KEY}:{SHOPIFY_API_SECRET}@{shop}/admin/api/{API_VERSION}/price_rules/{price_rule}/discount_codes.json'
    get_response = requests.get(discount_code_endpoint, headers=headers)
    discount_code_id=get_response.json()["discount_codes"][0]['id']

    patch_url = f"https://{shop}/admin/api/{API_VERSION}/price_rules/{price_rule}/discount_codes/{discount_code_id}.json"
    

    data = {
    "discount_code": {
        "id": discount_code_id,
        "code": discount_code,
      
    }
}
    discount_code_response = requests.patch(patch_url, json=data,headers=headers)
    if discount_code_response.status_code == 200:
        return Response({"success":discount_code_response.json()},status=status.HTTP_200_OK)
    else:
        return Response({"error":discount_code_response.json()},status=status.HTTP_400_BAD_REQUEST)
    


def coupon_validate(request):
    product_name=request.data.get("product_id")
    if not product_name:     
        return Response({'error': 'Product  field is required',"message":"Data not validate"}, status=status.HTTP_400_BAD_REQUEST)
    
    my_list = list(map(int, product_name.split(",")))
    
    influencer=request.data.get("influencer_name")
    if not influencer:
        return Response({'error': 'Influencer name  field is required',"message":"Data not validate"}, status=status.HTTP_400_BAD_REQUEST)


    discount = request.data.get('discount_code')
    if discount:
        if len(discount)<3:
            return Response({'error': 'discount code must be three or more than three character long',"message":"Data not validate"}, status=status.HTTP_400_BAD_REQUEST)

    if not discount:
        return Response({'error': 'discount code  field is required',"message":"Data not validate"}, status=status.HTTP_400_BAD_REQUEST)

    


    discount_type=request.data.get("discount_type")
    if not discount_type:
        return Response({'error': 'discount type field is required',"message":"Data not validate"}, status=status.HTTP_400_BAD_REQUEST)
    

    

    amount=request.data.get("amount")
    
    
    if not amount:
        return Response({'error': 'Amount field is required',"message":"Data not validate"}, status=status.HTTP_400_BAD_REQUEST)
    
    if int(amount)<1:
        return Response({"error":"Amount should be more than zero","message":"Data not validate"},status=status.HTTP_400_BAD_REQUEST)

    
   
    
    amt="-"+amount
    
    if amount and discount_type=="percentage":
        if float(amount) >100:
            return Response({'error': 'amount should be less than 100',"message":"Data not validate"}, status=status.HTTP_400_BAD_REQUEST)

    
    return Response({"message":"Data_Validate","amount":amount,"influencer":influencer,"discount":discount,"amount":amount,"amt":amt,"my_list":my_list,"discount_type":discount_type})


def marketcoupon_validate(request):
    product_name=request.data.get("product_id")
    if not product_name:     

        return Response({'error': 'Product field is required',"message":"Data not Validate"}, status=status.HTTP_400_BAD_REQUEST)
    my_list = list(map(int, product_name.split(",")))
    
    
    
    discount = request.data.get('discount_code')
    
    if discount:
        if len(discount)<3:
            return Response({'error': 'discount code must be three or more than three character long',"message":"Data not Validate"}, status=status.HTTP_400_BAD_REQUEST)

    if not discount:
        return Response({'error': 'Coupon field is required',"message":"Data not Validate"}, status=status.HTTP_400_BAD_REQUEST)
            
    discount_type=request.data.get("discount_type")
    if not discount_type:
        return Response({'error': 'discount_type field is required',"message":"Data not Validate"}, status=status.HTTP_400_BAD_REQUEST)
        
    amount=request.data.get("amount")

   
    if not amount:
        return Response({'error': 'Amount field is required',"message":"Data not Validate","message":"Data not Validate"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    if int(amount)<1:
        return Response({"error":"Amount should be more than zero","message":"Data not validate"},status=status.HTTP_400_BAD_REQUEST)
    
    amt_val="-"+amount

    return Response({"message":"Data_Validate","amount":amount,"discount":discount,"amount":amount,"amt_val":amt_val,"my_list":my_list,"discount_type":discount_type})
