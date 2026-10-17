from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Lead
from .serializers import LeadSerializer

class LeadListCreateView(generics.ListCreateAPIView):
    queryset = Lead.objects.all().prefetch_related("contact_owner")
    serializer_class = LeadSerializer
    # permission_classes = [IsAuthenticated]


class LeadDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all().prefetch_related("contact_owner")
    serializer_class = LeadSerializer
    # permission_classes = [IsAuthenticated]
