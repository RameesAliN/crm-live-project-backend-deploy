from rest_framework import serializers
from .models import Email


class EmailSerializer(serializers.ModelSerializer):
    
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
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def validate_subject(self, value):
        if not value.strip():
            raise serializers.ValidationError("Subject cannot be empty.")
        return value