from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView,  
    TokenVerifyView  
) 
from user import views as user_views
from institute import views as institute_views
from shop import views as shop_views
from Donor import views as donor_views

urlpatterns = [
    path('token/', user_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token-verify/', TokenVerifyView.as_view(), name='token_verify'),

    #Authentication Part:
    path('user/register/',user_views.RegisterView.as_view(),name='Register'),

    #Institute:
    path('institute_profile/',user_views.InstituteProfileCreateView.as_view(),name='institute_profile'),
    path('items/',institute_views.ItemListCreateView.as_view(), name='listcreate'),
    path('retrieve-items/<int:pk>/', institute_views.ItemRetrieveUpdateDestroyView.as_view(), name='item-detail'),
    path('institute-requests/', institute_views.InstituteRequestListCreateView.as_view(), name='institute-requests'),

    #Admin
    path('admin/institute-requests/', institute_views.InstituteRequestAdminListView.as_view(), name='admin-list-requests'),
    path('admin/institute-requests/<int:pk>/', institute_views.InstituteRequestAdminUpdateView.as_view(), name='admin-update-request'),


    #Donour
    path('donor_profile/',user_views.DonorProfileCreateView.as_view(),name='donor_profiel'),
    path('donations/', donor_views.DonationListCreateView.as_view(), name='donation-list-create'),
    path('donations/<int:pk>/', donor_views.DonationDetailView.as_view(), name='donation-detail'),   
    path("donate/", donor_views.DonationCreateView.as_view(), name="donation-create"),
    path("donation/payment-success/", donor_views.DonationPaymentSuccessView.as_view(), name="donation-payment-success"),


    #Shop
    path('shop_profile/',user_views.ShopProfileCreateView.as_view(),name='shop_profile'),
    path('store/create/', shop_views.StoreCreateView.as_view(), name='store-create'),
    path('store/<int:pk>/', shop_views.StoreDetailView.as_view(), name='store-detail'),
    path('stocks/add/', shop_views.StockCreateView.as_view(), name='add-stock'),
    path('stocks/', shop_views.StockListView.as_view(), name='list-stocks'), 
    path("create-order/", shop_views.ShopOrderCreateView.as_view(), name="create-order"),
    path("payment-success/", shop_views.PaymentSuccessView.as_view(), name="payment-success"),



]