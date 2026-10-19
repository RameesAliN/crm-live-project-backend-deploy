from rest_framework import serializers
from .models import Email


class EmailSerializer(serializers.ModelSerializer):

    created_by_name = serializers.SerializerMethodField()
    
    cc = serializers.ListField(
        child=serializers.EmailField(),
        required=False,
        default=list,
    )

    bcc = serializers.ListField(
        child=serializers.EmailField(),
        required=False,
        default=list,
    )

    class Meta:
        
        model = Email
        fields = [
            "id",
            "subject",
            "body",
            "recipient_email",
            "cc",
            "bcc",
            "lead",
            "company",
            "deal",
            "ticket",
            "created_by",
            "created_by_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_by",
            "created_by_name",
            "created_at",
            "updated_at",
        ]

    def validate_subject(self, value):
        if not value.strip():
            raise serializers.ValidationError("Subject cannot be empty.")
        return value

    def get_created_by_name(self,obj):
        if not obj.created_by:
            return None
        
        full_name = obj.created_by.get_full_name()
        return full_name or obj.created_by.email