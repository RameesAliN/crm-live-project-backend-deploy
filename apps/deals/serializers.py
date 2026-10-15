from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Deal
from apps.leads.models import Lead

User = get_user_model()
class UserDealSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "phone", "company_name"]

class LeadDealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ["id", "first_name", "last_name", "email", "phone"]

class DealSerializer(serializers.ModelSerializer):
    
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, coerce_to_string=False)
    
    owners = UserDealSerializer(many=True, read_only=True)
    owners_id = serializers.PrimaryKeyRelatedField(
    queryset=User.objects.all(),
    source="owners",
    many=True,
    write_only=True,
    required=True,
    )

    associated_lead = LeadDealSerializer(read_only=True)
    associated_lead_id = serializers.PrimaryKeyRelatedField(
    queryset=Lead.objects.all(),
    source="associated_lead",
    write_only=True,
    required=True,
    allow_null=False
    )
    
    class Meta:
        model = Deal
        fields = ["id", "deal_name", "associated_lead", "associated_lead_id", "stage", "amount", "priority", "close_date", "owners","owners_id", "created_at", "updated_at"]

