
from rest_framework import serializers
from .models import CallActivity


class CallActivitySerializer(serializers.ModelSerializer):
    lead_name = serializers.SerializerMethodField()
  
    time = serializers.TimeField(format="%H:%M:%S")

    created_by = serializers.SerializerMethodField()

    class Meta:
        model = CallActivity
        fields = [
            "id",
            "lead",
            "lead_name",
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
   