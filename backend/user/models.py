from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models



class User(AbstractUser):
    username = models.CharField(max_length=200,unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    
    role = models.CharField(
        max_length=20, 
        choices=[('institute', 'Institute'), ('donor', 'Donor'), ('shop', 'Shop'), ('admin', 'Admin')]
    )

    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions_set", blank=True)

    def __str__(self):
        return self.username
    
    def save(self,*args,**kwargs):
        email_username , mobile = self.email.split("@")

        if self.full_name == "" or self.full_name == None:
            self.full_name = email_username
        if self.username == "" or self.username == None:
            self.username = email_username
        super(User,self).save(*args,**kwargs)
    
class InstituteProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="institute_profile")
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    registration_number = models.CharField(max_length=50, help_text="Unique registration number",null=True,blank=True)
    institute_description = models.TextField(help_text="Provide a detailed description of the institute",null=True,blank=True)
    institute_size = models.PositiveIntegerField(help_text="Number of people in the institute",default=0)

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class InstituteDocument(models.Model):
    institute = models.ForeignKey(InstituteProfile, on_delete=models.CASCADE, related_name="documents")
    document = models.FileField(upload_to="institute_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.institute.name}"


class DonorProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donor_profile")
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    preferred_donation_category = models.TextField(help_text="Preferred items for donation", null=True, blank=True)

    def __str__(self):
        return self.full_name if self.full_name else "Unnamed Donor"



class ShopProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shop_profile")
    shop_name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.shop_name 
    

