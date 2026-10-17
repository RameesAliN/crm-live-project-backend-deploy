from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.products.models import Product
from apps.companies.models import Company
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
class ProductSerializer(serializers.ModelSerializer): 
    class Meta:
         model = Product 
         fields = ["id", "name","price"]



class LeadSerializer(serializers.ModelSerializer):
    contact_owner_name = serializers.SerializerMethodField()
    contact_owner = serializers.PrimaryKeyRelatedField( 
    queryset=User.objects.all(), many=True, required=False, )
    product_id = serializers.PrimaryKeyRelatedField(
    queryset=Product.objects.all(),source="products", many=True, required=False,write_only=True, )
    products = ProductSerializer(  many=True, read_only=True, )
    company = serializers.SlugRelatedField( 
        slug_field="company_name", 
        queryset=Company.objects.all(), required=False, allow_null=True, )

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
            "product_id",
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


