from django.urls import path
from AdminApp.views import *
from AdminApp.utils import *

urlpatterns = [
    # path("login/",Login.as_view(),name="login"),
    path('profile/update/<int:pk>/', ProfileUpdate.as_view(),name="profile_update"),

    # influencer api
    path("influencer/list/",InfluencerViewSet.as_view({'get': 'list'}),name="influencerview"),
    path("influencer/create/",InfluencerViewSet.as_view({'post': 'create'}),name="influencercreate"),
    path("influencer/edit/<int:pk>/",InfluencerViewSet.as_view({'put': 'update'}),name="InfluencerUpdate"),
    path("influencer/delete/<int:pk>/",InfluencerViewSet.as_view({'delete': 'destroy'}),name="InfluencerUpdate"),


    # Campaign api
    path("campaign/list/",CampaignViewSet.as_view({'get': 'list'}),name="influencer_view"),
    path('campaign/create/', CampaignViewSet.as_view({'post': 'create'}),name="campaign_create"),
    path('campaign/edit/<int:pk>/', CampaignViewSet.as_view({'put': 'update'}),name="campaign_update"),
    path('campaign/delete/<int:pk>/', CampaignViewSet.as_view({'delete': 'destroy'}),name="campaign_update"),



    # path("logout/",LogoutView.as_view(),name="logout"),
    path("dashboard",show,name="dashboard"),
	path('login1/',login_user,name="login1"),
    path('logout1/',logout_,name="logout1"),
    path('profile/',profile_update,name="profile"),
    path('campaign_data/',campaign_list,name="campaigndata"),
    path('market_data/',marketplace_list,name="marketdata"),
    path('vendor/',vendor_list,name="vendor_data"),
    path('vendor/<int:id>/',Single_Vendor,name="vendordetails"),
    path('campaign/<int:id>/',Single_camp,name="campaigndetails"),
    path('status/',change_status,name="status"),
    path("vendor/order/<int:id>",Order_list,name="order"),
    path("influencer_list/",Influencer_list,name="influencer_list"),
    path('inf_name/',influencer_name,name="inf_name"),
    path('pro_name/',product_name,name="pro_name"),
    path("forgot_password",forgot_password,name="forgot_password"),
    path("change_password_link/<str:email>/<int:token>",change_password_link,name="change_password_link"),
    path('split-payment/', split_payment, name='split_payment'),
    path('stripe/', stripe_data, name='stripe'),
    path('commission/', charge_commission, name='commission'),
    # path('get-coupon/', get_coupon_codes, name='get-coupon'),
    # path('campaign_accept/<int:id>', influenceraccept, name='campaign-accept'),
    # path('campaign_decline/<int:id>', influencerdecline, name='campaign-decline'),
    path('infldec/', admin_decision, name='infldec'),
    path('total_sales/', total_sales, name='total_sales'),
    path('payment_details/', paymentdetails, name='payment_details'),
    path('notified/', adminnotification, name='notified'),
    path('refund', Refundmoney, name='refund'),
    path('paid', Influncerpaid, name='paid'),
    path('total_balance', TotalPayment, name='total_balance'),
    path('marketpaid', MarketInfluncerpaid, name='marketpaid'),
    path('commission2', UpdateCommission, name='commission2'),


]