from datetime import date
from CampaignApp.models import Campaign
from CampaignApp.models import Product_information
from CampaignApp.models import Product_information
from ShopifyApp.models import influencer_coupon
from Affilate_Marketing.settings import base_url ,headers ,SHOPIFY_API_KEY,SHOPIFY_API_SECRET,API_VERSION


today = date.today()
def update_campaign_status():
    
    campaigns = Campaign.objects.filter(end_date__lt=today).update(campaign_exp=0)
    # product_info=Product_information.objects.filter(campaignid_id__campaign_exp=0).values_list("coupon_name")
    # for coup in product_info:
        
    #     delete_coup=influencer_coupon.objects.filter(coupon_name__in=coup).delete()
        
    #     url =f'https://{SHOPIFY_API_KEY}:{SHOPIFY_API_SECRET}@{acc_tok[1]}/admin/api/{API_VERSION}/price_rules/{price_rule}.json'

    
    
    
    
    
    
    
   
    
    
    
    
