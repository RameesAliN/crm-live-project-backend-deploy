from django.urls import path
from .views import (
    CallActivityListCreateView,
    CallActivityDetailView,
)

urlpatterns = [
    path("", CallActivityListCreateView.as_view(), name="call-activity-list-create"),
    path("<int:pk>/", CallActivityDetailView.as_view(), name="call-activity-detail"),
]