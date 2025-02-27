from django.shortcuts import render
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework  import generics,status
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import *

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainSerializer



class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
    permission_classes=(AllowAny,)


class InstituteProfileCreateView(generics.CreateAPIView):
    queryset = InstituteProfile.objects.all()
    serializer_class = InstituteProfileSerializer
    permission_classes = [AllowAny,]


    def perform_create(self, serializer):
        default_user = User.objects.first()  
        serializer.save(user=default_user)

    #We have to done this when we are connecting backend.
    #def perform_create(self, serializer):
       # serializer.save(user=self.request.user)

class DonorProfileCreateView(generics.CreateAPIView):
    queryset = DonorProfile.objects.all()
    serializer_class = DonorProfileSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
class ShopProfileCreateView(generics.CreateAPIView):
    queryset=ShopProfile.objects.all()
    serializer_class=ShopProfileSerializer

    def create(self,request,*args,**kwargs):
        return super().create(request, *args, **kwargs)
