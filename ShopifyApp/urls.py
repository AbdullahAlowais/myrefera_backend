from django.urls import path
from ShopifyApp.views import *

urlpatterns = [

  
  #SHOPIFY APPS URLS
  path("create/code/",CreateDiscountCodeView.as_view(),name="discountcode"),
  path("coupon/list/",DiscountCodeView.as_view(),name="couponlist"),
  path('coupon/delete/', DeleteCodeView.as_view(), name='delete'),
  path('coupon/edit/', EditCodeView.as_view(), name='edit'),
  path('single/data/', SingleCoupon.as_view(), name='single'),
  path('particular/product/', ParticularProduct.as_view(), name='particular'),
  path('particular/edit/', ProductEditCodeView.as_view(), name='partedit'),
  path('particular/discount/', ParticularDiscountCodeView.as_view(), name='partdisct'),
  path('analytics',Analytics.as_view(), name='analytics'),
  path('coupons/', ShopifyCouponView.as_view(), name='shopify-coupons'),
  path('coupons/', ShopifyCouponView.as_view(), name='shopify-coupons'),
]