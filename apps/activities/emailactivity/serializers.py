from rest_framework import serializers
from django.db import transaction
from .models import Email
from apps.attachments.models import Attachment
from apps.attachments.serializers import AttachmentSerializer


RECORD_FIELDS = ("lead", "company", "deal", "ticket")

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

    attachments = AttachmentSerializer(many=True, read_only=True)
    attachment_ids = serializers.PrimaryKeyRelatedField(
        queryset=Attachment.objects.all(), many=True, write_only=True, required=False,
    )
    files = serializers.ListField(child=serializers.FileField(), write_only=True, required=False)

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
            "attachments",
            "attachment_ids", 
            "files",
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

    def _record(self, data, key):
        if key in data:
            return data[key]
        return getattr(self.instance, key, None) if self.instance else None

    def validate(self, data):
        records = {k: self._record(data, k) for k in RECORD_FIELDS if self._record(data, k)}
        existing = data.get("attachment_ids", [])
        files = data.get("files", [])

        if (existing or files) and not records:
            raise serializers.ValidationError(
                "Link the email to a lead, company, deal or ticket before attaching files."
            )

        for attachment in existing:
            for key, record in records.items():
                if getattr(attachment, f"{key}_id") != record.id:
                    raise serializers.ValidationError(
                        f"Attachment {attachment.id} does not belong to this {key}."
                    )
        return data

    def _attach(self, email, existing, files):
        if existing:
            email.attachments.add(*existing)
        user = self.context["request"].user
        for upload in files:
            attachment = Attachment.objects.create(
                file=upload,
                original_name=upload.name,
                uploaded_by=user,
                lead=email.lead, company=email.company, deal=email.deal, ticket=email.ticket,
            )
            email.attachments.add(attachment)

    @transaction.atomic
    def create(self, validated_data):
        existing = validated_data.pop("attachment_ids", [])
        files = validated_data.pop("files", [])
        email = super().create(validated_data)
        self._attach(email, existing, files)
        return email

    @transaction.atomic
    def update(self, instance, validated_data):
        existing = validated_data.pop("attachment_ids", None)
        files = validated_data.pop("files", [])
        email = super().update(instance, validated_data)
        if existing is not None:
            email.attachments.set(existing)
        self._attach(email, [], files)
        return email