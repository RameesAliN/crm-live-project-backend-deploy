from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from apps.deals.serializers import DealSummarySerializer
from apps.leads.serializers import UserLeadSerializer
from apps.companies.serializers import CompanySerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={"input_type": "password"}
    )

    confirm_password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "company_name",
            "industry_type",
            "requested_role",
            "country",
            "password",
            "confirm_password",
        ]
        read_only_fields = ["id"]
    def validate(self, attrs):
            if attrs["password"] != attrs["confirm_password"]:
                raise serializers.ValidationError({"confirm_password": "Passwords do not match." })
    
            return attrs
    
    def create(self, validated_data):
            validated_data.pop("confirm_password")
            password = validated_data.pop("password")
            requested_role = validated_data.pop("requested_role", "employee")
    
            user = User.objects.create_user(
                password=password,
                role="employee",
                requested_role=requested_role,
                role_approved=(requested_role == "employee"),
                **validated_data
            )
    
            return user


#user serlzr
        
class UserSerializer(serializers.ModelSerializer): 
    leads = UserLeadSerializer( source="owned_leads", many=True, read_only=True, ) 
    deals = DealSummarySerializer(many=True, read_only=True)
    class Meta: 
        model = User 
        fields = [ "id", "first_name", "last_name", "email", "phone", "company_name", "industry_type", "requested_role", "country", "leads", "deals", ] 
        read_only_fields = ["id", "leads", "deals"]

   