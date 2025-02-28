from rest_framework import serializers
from .models import Donation

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = [
            'id', 'donor', 'amount_donated', 'transaction_id', 
            'payment_status', 'timestamp'
        ]
        read_only_fields = ['id', 'payment_status', 'timestamp']



