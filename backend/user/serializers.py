from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

ROLE_CHOICES = [
    ('institute', 'Institute'),
    ('donor', 'Donor'),
    ('shop', 'Shop'),
    ('admin', 'Admin'),
]


class MyTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)
        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username
        token['role'] = user.role

        return token
    


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password])
    password2 = serializers.CharField(write_only=True,required=True)
    role = serializers.ChoiceField(choices=ROLE_CHOICES)


    class Meta:
        model=User
        fields=[
            'username',
            'email',
            'phone',
            'password',
            'password2',
            'role',
        ]
    
    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"Password not matched"})
        return attrs
    
    def create(self,validated_data):
        role = validated_data.pop('role')  

        user = User.objects.create(
            username=validated_data['username'],
            email = validated_data['email'],
            phone = validated_data['phone'],
            role=role,
        )
        user.full_name=validated_data['username']
        user.set_password(validated_data['password'])
        user.save()
        if role == "institute":
            InstituteProfile.objects.create(user=user,name=user.username,phone=validated_data['phone'])  

        elif role=="donor":
            DonorProfile.objects.create(user=user,full_name=validated_data['username'],phone=validated_data['phone'])
        
        elif role=="shop":
            ShopProfile.objects.create(user=user,phone=validated_data['phone'])

        return user


class InstituteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteProfile
        fields = [
            'id',
            'user',
            'name',
            'address',
            'phone',
            'registration_number',
            'institute_description',
            'institute_size',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class DonorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonorProfile
        fields = '__all__'


class ShopProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= ShopProfile
        fields = '__all__'