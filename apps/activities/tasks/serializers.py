from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.SerializerMethodField()
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
            "assigned_to_name",
            "lead",
            "company",
            "deal",
            "ticket",
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

    def get_assigned_to_name(self, obj):
        if obj.assigned_to:
            return f"{obj.assigned_to.first_name} {obj.assigned_to.last_name}".strip()
        return None

    
    def validate(self, attrs):
        instance = self.instance

        lead = attrs.get("lead",instance.lead if instance else None,)
        company = attrs.get("company", instance.company if instance else None,)
        deal = attrs.get("deal",instance.deal if instance else None,)
        ticket = attrs.get("ticket", instance.ticket if instance else None)

        selected = [lead, company, deal, ticket]

        if sum(value is not None for value in selected) != 1:
            raise serializers.ValidationError("A task must belong to exactly one: Lead, Company, Deal, or Ticket.")
        return attrs