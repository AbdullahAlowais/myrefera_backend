from django.urls import path
from InfluencerApp.views import *


urlpatterns = [
    
    #LOGIN/REGISTER URLS
    path("create/",Register.as_view(),name="influencer_register"),
    path("influencer/details/",Details.as_view(),name="details"),
    path("login/",InfluencerLogin.as_view(),name="influencer_login"),
    path("activate/<token>/<id>",VerificationView.as_view(),name="activate"),
    path("pending/",PendingList.as_view(),name="pending"),
    path("approval/",ApprovalList.as_view(),name="approval"),
    path("single/<int:id>/",GetCampaign.as_view(),name="single"),
    path("decline/",DeclinelList.as_view(),name="single"),
    path("step/one",StepOneAPIView.as_view(),name="one"),
    path("step/two",StepTwoAPIView.as_view(),name="two"),
     
     
    #INFLUENCER SHOW/EDIT/Logout URLS
    path('influencer/list/', InfluencerList.as_view(),name="Influencer-list"),
    path('details/', InfluencerData.as_view(),name="Influencer-details"),
    path("influencer/update/<int:pk>/",UpdateInfluencer.as_view(),name="UpdateInfluencer"),  
    path('influencer/logout/', LogoutView.as_view(), name='logout'),
    path('transfer/', InfluencerTransfer.as_view(), name='transfer'),
    
    

    
    
    #INFLUENCER CAMPAGIN APIS URLS
    path('accept/<int:id>/', AcceptView.as_view(), name='accept'),
    path('decline/<int:id>/', DeclineView.as_view(), name='decline'),
    path('influencer/campaign/', PendingCampaing.as_view(), name='campaign'),
    path('notification/', VendorNotification.as_view(), name='notification'),
    path('change/status/', ChangeNotifStatus.as_view(), name='status'),
   
    #strip urls
    path('stripe/connect/', StripeConnectAccountView.as_view(), name='stripe-connect'),
    path('stripe/customer/', CustomerCreate.as_view(), name='stripe-cutomer'),
    path('stripe/payment/', CreatePaymentIntent.as_view(), name='stripe-payment'),
    path('stripe/token/', StripeToken.as_view(), name='stripe-token'),
    path('stripe/verify/', Stripeverify.as_view(), name='stripe-verify'),
    path('stripe/details/', InfluencerStripe.as_view(), name='stripe-details'),


    #lean urls
    path('lean/customers/', LeanCustomer.as_view(), name='lean-customers'),
    path('lean/endcustomers/', LeanEndCustomer.as_view(), name='lean-endcustomers'),
    path('customers/data', GetCustomer.as_view(), name='customers-data'),
    path('entity/', GetEntity.as_view(), name='entity'),
    path('destination/list/', DestinationList.as_view(), name='destination-list'),
    path('lean/destination/', LeanDestination.as_view(), name='lean-destination'),
    path('payment/list/', PaymentList.as_view(), name='payment-list'),
    path('bank/list/', BankList.as_view(), name='bank-list'),
    path('paymentintent/list/', PaymnetIntentist.as_view(), name='payment-intent'),
    path('verify/name/', VerifyName.as_view(), name='verify-name'),
    path('lean/entity/', value, name='lean-destination'),
    path('bank/account/', create_bank_account_token.as_view(), name='bank-account'),
    path('stripe/platform', CreateConnectedAccountView.as_view(), name='bank-account'),
    path('infl_data/', InfluencerData.as_view(), name='bank-infl_data'),
    path('vendor_key/', Vendorkey.as_view(), name='bank-vendor_key'),
    path('click/', Click_analytics.as_view(), name='bank-click'),
    path('dubai/', Dubaiaccount.as_view(), name='dubai'),
    path('admindec/', Admindecision.as_view(), name='admindec'),
    path('inflapplied/', InfluencerApplied.as_view(), name='inflapplied'),
    path('applied/', AppliedCampaign.as_view(), name='applied'),
    path('inflprofile/', InfluencerProfile.as_view(), name='inflprofile'),
    path('inflmarketaccept/', MarketplaceAccept.as_view(), name='inflmarketaccept'),
    path('inflmarketdecline/', MarketplaceDeclinelList.as_view(), name='inflmarketdecline'),
    path('influsersales/', InfluencerSaledata.as_view(), name='influsersales'),
    path('amounttransfer/', AmountTransfer.as_view(), name='amounttransfer'),
    

    
]   