from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone

from .models import Email
from .serializers import EmailSerializer


class EmailAccessMixin:
    permission_classes = [IsAuthenticated]
    serializer_class = EmailSerializer

    def get_queryset(self):
        queryset = Email.objects.select_related("lead", "company", "deal", "ticket", "created_by")

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

        return queryset.order_by("-created_at")


class EmailListCreateView(EmailAccessMixin, generics.ListCreateAPIView):
    
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class EmailDetailView(EmailAccessMixin, generics.RetrieveUpdateDestroyAPIView):
    pass

class EmailSendView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,pk):
        try:
            email = Email.objects.prefetch_related("attachments").get(pk=pk)
        except Email.DoesNotExist:
            return Response(
                {"detail" : "Email not found"},
                status = status.HTTP_404_NOT_FOUND
            )

        if email.sent_at:
            return Response(
                {"detail": "This email has already been sent."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            return Response(
                {"detail": "SMTP credentials are not configured."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        try:
            message = EmailMessage(
                subject=email.subject,
                body=email.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email.recipient_email],
                cc=email.cc or [],
                bcc=email.bcc or [],
            )

            for attachment in email.attachments.all():
                attachment.file.open("rb")
                try:
                    message.attach(
                        attachment.original_name or attachment.file.name.split("/")[-1],
                        attachment.file.read(),
                    )
                finally:
                    attachment.file.close()

            message.send(fail_silently=False)

            email.sent_at = timezone.now()
            email.save(update_fields=["sent_at"])

            return Response(
                EmailSerializer(email).data,
                status=status.HTTP_200_OK,
            )

        except Exception:
            return Response(
                {"detail": "Email sending failed. Check SMTP configuration and server logs."},
                status=status.HTTP_502_BAD_GATEWAY,
            )