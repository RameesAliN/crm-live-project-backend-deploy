from django.urls import path
from .views import EmailListCreateView, EmailDetailView,EmailAttachmentListCreateView,EmailSendView

urlpatterns = [
    path("", EmailListCreateView.as_view(), name="email-list-create"),
    path("<int:pk>/", EmailDetailView.as_view(), name="email-detail"),
    path("<int:email_id>/emailattachments/", EmailAttachmentListCreateView.as_view(), name="email-attachment-list-create"),
    path("<int:pk>/send/", EmailSendView.as_view(), name="email-send")
]

