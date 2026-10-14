from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Lead
# from .models import Lead

User = get_user_model()

class UserLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "lead_status",
            "company",
            "created_date",
        ]



class LeadSerializer(serializers.ModelSerializer):
    contact_owner_name = serializers.SerializerMethodField()
    contact_owner = serializers.PrimaryKeyRelatedField( 
        queryset=User.objects.all(), many=True, required=False, )

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

    def get_contact_owner_name(self, obj) -> list[str]:
          names = []

          for owner in obj.contact_owner.all():
            full_name = owner.get_full_name()
            names.append(full_name )

          return names


