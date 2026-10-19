
from django.urls import path, include

urlpatterns = [
    path("", include("apps.users.urls")),
    path("leads/", include("apps.leads.urls")),
    path("", include("apps.deals.urls")),
    path("companies/", include("apps.companies.urls")),
    path("products/",include("apps.products.urls")),

    path ("tickets/",include("apps.tickets.urls")),
    path("meetings/", include("apps.meetingactivity.urls")),
    path("emails/", include("apps.emailactivity.urls")),
    path("calls/",include("apps.callActivity.urls")),
    path("notes/", include("apps.activities.notes.urls")),
    path("tasks/", include("apps.activities.tasks.urls")),
]
