from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Meeting
from .serializers import MeetingSerializer


class MeetingAccessMixin:
    permission_classes = [IsAuthenticated]
    serializer_class = MeetingSerializer

    def get_queryset(self):
        queryset = Meeting.objects.select_related("lead", "company", "deal", "ticket", "created_by")

        lead_id = self.request.query_params.get("lead")
        company_id = self.request.query_params.get("company")
        deal_id = self.request.query_params.get("deal")
        ticket_id = self.request.query_params.get("ticket")

        if lead_id:
            queryset = queryset.filter(lead_id=lead_id)
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        if deal_id:
            queryset = queryset.filter(deal_id=deal_id)
        if ticket_id:
            queryset = queryset.filter(ticket_id=ticket_id)

        return queryset


class MeetingListCreateView(MeetingAccessMixin, generics.ListCreateAPIView):
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class MeetingDetailView(MeetingAccessMixin, generics.RetrieveUpdateDestroyAPIView):
    pass