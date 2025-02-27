from rest_framework import serializers
from .models import AdminRequestQueue

class AdminRequestQueueSerializer(serializers.ModelSerializer):
    institute_name = serializers.CharField(source='institute_request.institute.username', read_only=True)
    item_name = serializers.CharField(source='institute_request.item.name', read_only=True)
    quantity = serializers.IntegerField(source='institute_request.quantity', read_only=True)
    request_status = serializers.CharField(source='institute_request.status', read_only=True)

    class Meta:
        model = AdminRequestQueue
        fields = [
            'id', 'institute_request', 'institute_name', 'item_name', 'quantity', 
            'request_status', 'status', 'added_at', 'processed_at', 'completed_at'
        ]
        read_only_fields = ['added_at', 'processed_at', 'completed_at']
