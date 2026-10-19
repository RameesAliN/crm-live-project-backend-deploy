from rest_framework import serializers
from .models import Note,Task


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


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "task_name",
            "due_date",
            "due_time",
            "task_type",
            "priority",
            "note",
            "assigned_to",
            "lead",
            "company",
            "deal",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_task_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Task name cannot be empty.")
        return value

    def validate_note(self, value):
        if not value.strip():
            raise serializers.ValidationError("Note cannot be empty.")
        return value

    
    def validate(self, attrs):
        instance = self.instance

        lead = attrs.get("lead",instance.lead if instance else None,)
        company = attrs.get("company", instance.company if instance else None,)
        deal = attrs.get("deal",instance.deal if instance else None,)

        selected = [lead, company, deal]

        if sum(value is not None for value in selected) != 1:
            raise serializers.ValidationError("A task must belong to exactly one: Lead, Company, or Deal.")
        return attrs
    
