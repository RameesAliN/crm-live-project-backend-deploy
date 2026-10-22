from rest_framework import serializers
from .models import Email,EmailAttachment

class EmailAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAttachment
        fields = ["id", "email", "file", "uploaded_at"]
        read_only_fields = ["id", "email", "uploaded_at"]

class EmailSerializer(serializers.ModelSerializer):

    emailattachments = EmailAttachmentSerializer(many=True, read_only=True)
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
            "emailattachments",
            "sent_at",
            "created_by",
            "created_by_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "sent_at",
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

