from rest_framework import serializers
from .models import *

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "owner", "name", "location", "created_at"]

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'store', 'product_name', 'quantity', 'price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']



class ShopOrderSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source="store.name", read_only=True)
    institute_name = serializers.CharField(source="institute_request.institute.name", read_only=True)  # Assuming InstituteRequest has an institute field

    class Meta:
        model = ShopOrder
        fields = [
            "id",
            "store",
            "store_name",
            "institute_request",
            "institute_name",
            "total_amount",
            "status",
            "payment_status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "status", "payment_status", "created_at", "updated_at"]