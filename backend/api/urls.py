from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView,  
    TokenVerifyView  
)
from user import views as user_views

urlpatterns = [
    path('token/', user_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token-verify/', TokenVerifyView.as_view(), name='token_verify'),

    #Authentication Part:
    path('user/register/',user_views.RegisterView.as_view(),name='Register'),

    #Institute:
    path('institute_profile/',user_views.InstituteProfileCreateView.as_view(),name='institute_profile'),

    #Donour
    path('donor_profile/',user_views.DonorProfileCreateView.as_view(),name='donor_profiel'),

    #Shop
    path('shop_profile/',user_views.ShopProfileCreateView.as_view(),name='shop_profile'),

]