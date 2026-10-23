from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from .models import Attachment
from .serializers import AttachmentSerializer


class AttachmentViewSet(viewsets.ModelViewSet):
    
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        queryset = Attachment.objects.select_related("uploaded_by")
        for param in ("lead", "company", "deal", "ticket"):
            value = self.request.query_params.get(param)
            if value:
                queryset = queryset.filter(**{f"{param}_id": value})
        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        upload = self.request.FILES["file"]
        serializer.save(uploaded_by=self.request.user, original_name=upload.name if upload else "",)
