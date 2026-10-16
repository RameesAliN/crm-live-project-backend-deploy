from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Company


User = get_user_model()



class CompanySerializer(serializers.ModelSerializer):
    company_owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True,)

    company_owner_name = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = [
            "id",
            "domain",
            "company_name",
            "company_owner",
            "company_owner_name",
            "industry",
            "type",
            "city",
            "country_region",
            "no_of_employees",
            "annual_revenue",
            "country_code",
            "phone_number",
            "created_date",
            "updated_date",
        ]

        read_only_fields = [
            "id",
            "created_date",
            "updated_date",
        ]

    def get_company_owner_name(self, obj):
      if obj.company_owner:
        return f"{obj.company_owner.first_name} {obj.company_owner.last_name}".strip()


      return None