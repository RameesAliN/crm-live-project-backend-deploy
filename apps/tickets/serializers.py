from rest_framework import serializers

from .models import Ticket
from apps.deals.models import Deal
from apps.leads.models import Lead

class LeadDetailsSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()
    class Meta:
        model = Lead
        fields = [
        "id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "lead_status",
        ]
    def get_phone(self, obj):
         if obj.country_code and obj.phone:
            return f"{obj.country_code} {obj.phone}"
         return obj.phone or ""


class DealDetailsSerializer(serializers.ModelSerializer):
    leads = LeadDetailsSerializer(
    source="associated_lead",
    read_only=True,
    )


    class Meta:
        model = Deal
        fields = [
        
            "deal_name",
            "leads",
        ]


class TicketSerializer(serializers.ModelSerializer):
    ticket_owners = serializers.SerializerMethodField()
    deal_details = DealDetailsSerializer(
        source="deal",
        read_only=True,
    )

    class Meta:
        model = Ticket
        fields = [
            "id",
            "ticket_name",
            "description",
            "priority",
            "ticket_status",
            "ticket_owner",
            "ticket_owners",
            "deal",
            "deal_details",
            "created_at",
            "updated_at",
        ]

    def get_ticket_owners(self, obj):
        return [
            user.get_full_name() or user.email
            for user in obj.ticket_owner.all()
        ]
