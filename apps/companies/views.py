from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Company
from .serializers import CompanySerializer


class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all().prefetch_related("company_owner")
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]


class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all().prefetch_related("company_owner")
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]