from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from .models import CallActivity
from .serializers import CallActivitySerializer


class CallActivityListCreateView(generics.ListCreateAPIView):
    serializer_class = CallActivitySerializer

    def get_queryset(self):
        queryset = CallActivity.objects.select_related(
            "lead",
            "created_by"
        ).all()

        lead_id = self.request.query_params.get("lead")

        if lead_id:
            queryset = queryset.filter(lead_id=lead_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CallActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CallActivity.objects.select_related(
        "lead",
        "created_by"
    ).all()
    serializer_class = CallActivitySerializer
    