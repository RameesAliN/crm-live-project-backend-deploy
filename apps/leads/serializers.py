from rest_framework import serializers
from .models import Lead

class LeadSerializer(serializers.ModelSerializer):
    contact_owner_name = serializers.SerializerMethodField()

    class Meta:
        model = Lead
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "country_code",
            "phone",
            "job_title",
            "city",
            "country",
            "lead_status",
            "contact_owner",
            "contact_owner_name",
            "products",
            "company",
            "created_date",
            "updated_date",
        ]

        read_only_fields = ["id", "created_date", "updated_date"]

    def get_contact_owner_name(self, obj):
        if obj.contact_owner:
            return obj.contact_owner.get_full_name()
        return None
