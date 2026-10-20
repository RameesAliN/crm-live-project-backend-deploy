from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = [
            "id",
            "content",
            "lead",
            "company",
            "deal",
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

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Note cannot be empty.")
        return value