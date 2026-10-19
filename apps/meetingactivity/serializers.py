from rest_framework import serializers
from .models import Meeting


class MeetingSerializer(serializers.ModelSerializer):
    duration_minutes = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Meeting
        fields = [
            "id", "title", "start_time", "end_time", "duration_minutes",
            "attendees", "location", "reminder", "note",
            "lead", "company", "deal", "ticket",
            "created_by","created_by_name", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_by","created_by_name", "created_at", "updated_at"]

    def get_duration_minutes(self, obj):
        delta = obj.end_time - obj.start_time
        return int(delta.total_seconds() // 60)

    def validate(self, data):
        if data.get("end_time") and data.get("start_time") and data["end_time"] <= data["start_time"]:
            raise serializers.ValidationError("End time must be after start time.")
        return data

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def get_created_by_name(self,obj):
            if not obj.created_by:
                return None
            
            full_name = obj.created_by.get_full_name()
            return full_name or obj.created_by.email