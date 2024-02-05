from rest_framework import serializers
from CampaignApp.models import *
from django.contrib.auth.hashers import make_password
import ast


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True,required=True)
    

    def create(self, validated_data):
        
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        validated_data['password'] = make_password(password)       
        return super(RegisterSerializer, self).create(validated_data) 
    
    
    class Meta:
        
        model=User
        fields=["id","username","email","phone_number","password","user_type","confirm_password","shopify_url","instagram_url","category","image"]
        extra_kwargs = {
            'password': {'required': True},
            'email': {'required': True},
            'confirm_password': {'required': True},
            'shopify_url': {'required': True},
            'instagram_url': {'required': True},
            'category': {'required': True},
            'username': {'required': True},
            'image':{'required':False},
            'phone_number':{'required':True},
        }
    
    def validate_password(self,password):
        
                # if password != confirm_password:
                #     raise serializers.ValidationError('Password must match')
            if len(password)< 8:
                raise serializers.ValidationError("Password must be more than 8 character.")
            if not any(char.isdigit() for char in password):
                raise serializers.ValidationError('Password must contain at least one digit.')
            return password
        
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Password fields did not match.")
        return attrs
   
    def validate_shopify_url(self,shopify_url):
        if "//" in shopify_url or "/" in shopify_url:
            raise serializers.ValidationError("Please enter url name")
        
        if shopify_url == "":
            raise serializers.ValidationError("Shopify_url cannot be empty")
            
        return shopify_url
    def validate_instagram_url(self,instagram_url):
        if instagram_url == "":
            raise serializers.ValidationError("instagram_url cannot be empty")
            
        return instagram_url
    
    
class CommaSeparatedField(serializers.CharField):
    def to_internal_value(self, data):
        if not data:
            return []
        data_list=data.split(",")
        
        int_list = [int(num) for num in data_list]
        return int_list

class StrCommaSeparatedField(serializers.CharField):
    def to_internal_value(self, data):
        if not data:
            return []
        data_list=data.split(",")
        
        int_list = [(num) for num in data_list]
        return int_list


class CampaignSerializer(serializers.ModelSerializer):
  
   class Meta:
        model=Campaign
        fields = ['id','image','campaign_name',"date","description","influencer_visit","campaign_name","end_date","payout_amount","influencer_fee","offer"]
        extra_kwargs = {
                'campaign_name': {'required': True},
                'date': {'required': True},
                'end_date': {'required': True},
                #'influencer_name': {'required': True},
                "payout_amount":{'required': False},
                "influencer_fee":{'required': False},
                "offer":{'required': False},
                "image":{'required': False},
            
            }
 
   def validate_influencer_fee(self,influencer_fee):
       
        offer = self.initial_data.get('offer')
       
        if influencer_fee >100 and offer=="percentage":
            raise serializers.ValidationError("Influencer fee must be less than or equal to 100.")
        
     

        return influencer_fee

    
    
class InflCampSerializer(serializers.ModelSerializer):
   influencer_name= CommaSeparatedField()

#    product_discount=CommaSeparatedField()
   class Meta:
        model=Campaign
        fields = ['id', 'campaign_name',"influencer_name","date","influencer_visit","offer","description","influencer_fee","end_date","payout_amount"]
        extra_kwargs = {
                'campaign_name': {'required': True},
                'influencer_visit': {'required': True},
                'offer': {'required': False},
                'influencer_name': {'required': True},
                'date': {'required': True},
                'end_date': {'required': True},
                "influencer_fee":{'required': False},
                "payout_amount":{'required': False},

                
            }

   def validate_influencer_fee(self,influencer_fee):
        
        offer = self.initial_data.get('offer')
      
        
        if influencer_fee >100 and offer=="percentage":
            raise serializers.ValidationError("Influencer fee must be less than or equal to 100.")
        
        if influencer_fee < 0 and offer=="percentage":
            raise serializers.ValidationError("Influencer fee must be in positive.")
        if influencer_fee < 0 and offer=="commission":
            raise serializers.ValidationError("Influencer fee must be in positive.")
        return influencer_fee


class CampaignUpdateSerializer(serializers.ModelSerializer):

   influencer_name= CommaSeparatedField(required=False) 
   class Meta:
        model=Campaign
        fields = ["id",'campaign_name','influencer_visit',"offer","date","description","influencer_name","influencer_fee","campaign_status","end_date","payout_amount"]
        extra_kwargs = {
        'campaign_name': {'required': False},
        'influencer_visit': {'required': False},
        'offer': {'required': False},
        'description': {'required': False},
        'influencer_name': {'required': False},
        'date': {'required': False},  
        'end_date': {'required': False},    
        'influencer_fee': {'required': False}, 
        'payout_amount': {'required': False},   
    }


   def validate_influencer_fee(self,influencer_fee):
        offer = self.initial_data.get('offer')
       
        if influencer_fee >100 and offer=="percentage":
            raise serializers.ValidationError("Influencer fee must be less than or equal to 100.")
        
        if influencer_fee < 0 and offer=="percentage":
            raise serializers.ValidationError("Influencer fee must be in positive.")
        if influencer_fee < 0 and offer=="commission":
            raise serializers.ValidationError("Influencer fee must be in positive.")
        return influencer_fee



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Productdetails()
        fields = ["coupon_name","product_name"]
        extra_kwargs={
            "coupon_name":{"required":True},
            "product_name":{"required":True}
        }

            

class GETSerializer(serializers.ModelSerializer):
   
   product = CommaSeparatedField()
    
   class Meta:
        model=Campaign
        fields = ['id','campaign_name',"offer","product_discount","product","date","description","influencer_visit","coupon","influencer_fee"]
        extra_kwargs = {
                'campaign_name': {'required': True},
                'date': {'required': True},
                #'influencer_name': {'required': True},
                'offer': {'required': True},
                'product': {'required': True},
                'product_discount': {'required': True},
                 "influencer_fee":{'required': False},
                
            
            }

    

class UpdateProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=False)

    
    def update(self, instance, validated_data):
        password = validated_data.get('password',None)
        
        if password:
            instance.password = validated_data.get('password', instance.password)
            validated_data['password'] = make_password(instance.password)   
        else:
            validated_data.pop('password', None)
  
        return super(UpdateProfileSerializer , self).update(instance,validated_data)
    
    
    
    class Meta:
        
        model=User
        fields=["id","username","email","phone_number","password","user_type","shopify_url","instagram_url","category","image"]
        extra_kwargs = {
            'password': {'required': False},
            'email': {'required': False},
            'shopify_url': {'required': False},
            'instagram_url': {'required': False},
            'category': {'required': False},
            'username': {'required': False},
            'image': {'required': False},
            'phone_number':{'required':True},
            'image':{'required':False},
        }
    
    def validate_password(self,password):
        
             
            if len(password)< 8:
                raise serializers.ValidationError("Password must be more than 8 character.")
            if not any(char.isdigit() for char in password):
                raise serializers.ValidationError('Password must contain at least one digit.')
            return password
        
   
    def validate_shopify_url(self,shopify_url):
        if "//" in shopify_url or "/" in shopify_url:
            raise serializers.ValidationError("Please enter url name")
        
        if shopify_url == "":
            raise serializers.ValidationError("Shopify_url cannot be empty")
            
        return shopify_url


    def validate_instagram_url(self,instagram_url):

        if instagram_url == "":
            raise serializers.ValidationError("instagram_url cannot be empty")
            
        return instagram_url
    
    

class InfluencerFollower(serializers.ModelSerializer):
    class Meta:
        model = ModashInfluencer
        fields="__all__"


class VendorStripeSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=VendorStripeDetails
        fields="__all__"
        extra_kwargs = {
            'publishable_key': {'required': True},
            'secret_key': {'required': True},
            
        }
        
    
    def validate_publishable_key(self,publishable_key):

        if publishable_key == "":
            raise serializers.ValidationError("publishable_key cannot be empty")
            
        return publishable_key
    
    
    def validate_secret_key(self,secret_key):

        if secret_key == "":
            raise serializers.ValidationError("secret_key cannot be empty")
            
        return secret_key