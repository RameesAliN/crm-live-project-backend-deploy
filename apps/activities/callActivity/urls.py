from django.urls import path
from .views import (
    CallActivityListCreateView,
    CallActivityDetailView,
    MakeCallView,
    MakeBridgeCallView,
    twiml_voice_view,
)

urlpatterns = [
    path("", CallActivityListCreateView.as_view(), name="call-activity-list-create"),
    path("<int:pk>/", CallActivityDetailView.as_view(), name="call-activity-detail"),
    path(
            "test-call/",
            MakeCallView.as_view(),
            name="test-twilio-call",
        ),
    path("bridge-call/", MakeBridgeCallView.as_view(), name="test-bride-call"),
]
