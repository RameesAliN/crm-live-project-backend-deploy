from rest_framework import serializers
from .models import Lead


from rest_framework import serializers
from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    contact_owner_name = serializers.CharField(
        source="contact_owner.username",
        read_only=True,
    )

    product_names = serializers.StringRelatedField(
        source="products",
        many=True,
        read_only=True,
    )

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
            "product_names",
            "company",
            "created_date",
            "updated_date",
        ]
        read_only_fields = ["id", "created_date", "updated_date"]
