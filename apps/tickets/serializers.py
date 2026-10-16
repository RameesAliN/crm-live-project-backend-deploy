
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Ticket

User = get_user_model()


class TicketSerializer(serializers.ModelSerializer):
    ticket_owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=False,
    )

    ticket_owner_name = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = "__all__"

    def get_ticket_owner_name(self, obj):
        return [
            user.get_full_name() or user.email
            for user in obj.ticket_owner.all()
        ]

