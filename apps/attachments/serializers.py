from rest_framework import serializers
from .models import Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    
    uploaded_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = ["id", "file", "original_name", "lead", "company", "deal", "ticket", "uploaded_by","uploaded_by_name", "created_at"]
        read_only_fields = ["id", "original_name", "uploaded_by","uploaded_by_name", "created_at"]

    def get_uploaded_by_name(self,obj):
        if obj.uploaded_by:
            return obj.uploaded_by.get_full_name() or obj.uploaded_by.email
        return None

    def validate(self, data):
        if self.instance is None:
            related_objects = (
                "lead",
                "company",
                "deal",
                "ticket",
            )

            if not any(data.get(field) for field in related_objects):
                raise serializers.ValidationError(
                    "Attach the file to a lead, company, deal or ticket."
                )

        return data