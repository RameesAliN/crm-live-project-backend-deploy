
from rest_framework import serializers
from .models import CallActivity


class CallActivitySerializer(serializers.ModelSerializer):
    lead_name = serializers.SerializerMethodField()
    # company_name = serializers.SerializerMethodField()
    # deal_name = serializers.SerializerMethodField()
    # ticket_name = serializers.SerializerMethodField()

    time = serializers.TimeField(format="%H:%M:%S")

    created_by = serializers.SerializerMethodField()

    class Meta:
        model = CallActivity
        fields = [
            "id",
            "lead",
            "leadname"
            "company",
            "deal",
            "ticket",
            "call_outcome",
            "duration",
            "date",
            "time",
            "note",
            "created_by",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def get_created_by(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name() or obj.created_by.email
        return None

    def get_lead_name(self, obj): 
        if obj.lead: return f"{obj.lead.first_name} {obj.lead.last_name}".strip()
        return None 
    # def get_company_name(self, obj):
    #      if obj.company: return obj.company.company_name 
    #      return None 
    # def get_deal_name(self, obj): 
    #     if obj.deal: return obj.deal.deal_name 
    #     return None 
    # def get_ticket_name(self, obj): 
    #     if obj.ticket: return obj.ticket.ticket_name 
    #     return None
