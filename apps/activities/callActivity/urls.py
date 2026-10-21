from django.urls import path
from .views import (
    CallActivityListCreateView,
    CallActivityDetailView,
    TestTwilioCallView,
    twiml_voice_view,
)

urlpatterns = [
    path("", CallActivityListCreateView.as_view(), name="call-activity-list-create"),
    path("<int:pk>/", CallActivityDetailView.as_view(), name="call-activity-detail"),
    path(
            "test-call/",
            TestTwilioCallView.as_view(),
            name="test-twilio-call",
        ),
    
]
