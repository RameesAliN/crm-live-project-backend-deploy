from django.urls import path
from .views import EmailListCreateView, EmailDetailView,EmailSendView

urlpatterns = [
    path("", EmailListCreateView.as_view(), name="email-list-create"),
    path("<int:pk>/", EmailDetailView.as_view(), name="email-detail"),
    path("<int:pk>/send/", EmailSendView.as_view(), name="email-send")
]

