from rest_framework import serializers
from .models import *
from django.utils import timezone

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class InstituteRequestSerializer(serializers.ModelSerializer):
    institute_name = serializers.CharField(source='institute.username', read_only=True)
    item_name = serializers.CharField(source='item.name', read_only=True)

    class Meta:
        model = InstituteRequest
        fields = [
            'id', 'institute', 'institute_name', 'item', 'item_name', 'quantity', 
            'status', 'approved_at', 'rejected_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['approved_at', 'rejected_at', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['institute'] = request.user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        new_status = validated_data.get('status', instance.status)

        if new_status == 'Approved' and instance.status != 'Approved':
            instance.approved_at = timezone.now()
            instance.rejected_at = None 
        elif new_status == 'Rejected' and instance.status != 'Rejected':
            instance.rejected_at = timezone.now()
            instance.approved_at = None  

        instance.status = new_status
        instance.save()
        return instance


class InstituteDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteDocument
        fields = ["id", "user", "document", "status", "uploaded_at", "reviewed_at", "rejection_reason"]
        read_only_fields = ["uploaded_at", "reviewed_at", "rejection_reason"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        user=User.objects.get(id=1)  #tempoorary use only make sure to delete when connecting frontend.
        if request and user.role == "institute":  # instead of user.role you need to add request.user.role 
            self.fields["status"].read_only = True
