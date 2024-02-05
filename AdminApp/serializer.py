from rest_framework import serializers
from AdminApp.models import *
from CampaignApp.models import *
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data.pop('password')
        # print(password)
        validated_data['password'] = make_password(password)       
     
        return super(UserSerializer, self).create(validated_data) 
    
    def update(self, instance, validated_data):
        instance.password = validated_data.get('password', instance.password)
        validated_data['password'] = make_password(instance.password)       
        return super(UserSerializer, self).update(instance,validated_data)
    
    
    class Meta:
        
        model=User
        fields=["username","email","password"]
        extra_kwargs = {
            'password': {'required': True},
            'username': {'required': True}
        }
    
    def validate_password(self,password):
        if len(password)< 8:
            raise serializers.ValidationError("Password must be more than 8 character.")
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError('Password must contain at least one digit.')
        return password


class UpdateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=False)
   
   
    def update(self, instance, validated_data):
        password = validated_data.get('password',None)
        
        if password:
            instance.password = validated_data.get('password', instance.password)
            validated_data['password'] = make_password(instance.password)   
        else:
            validated_data.pop('password', None)
  
        return super(UpdateUserSerializer , self).update(instance,validated_data)
    
    
    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Influencer with this email already exists")
        return lower_email
    
    class Meta:
        model=User
        fields=["username","email","password"]
        extra_kwargs = {
            'email': {'required': False},
            'username': {'required': False},
          
        }
    
    def validate_password(self,password):
        if len(password)< 8:
            raise serializers.ValidationError("Password must be more than 8 character.")
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError('Password must contain at least one digit.')
        return password



class UpdateCampaignSerializer(serializers.ModelSerializer):
      
    class Meta:
        model=Campaign
        fields = ['product_name', 'campaign_name',"influencer_name","coupon"]

