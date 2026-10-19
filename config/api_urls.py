
from django.urls import path, include

urlpatterns = [
    path("", include("apps.users.urls")),
    path("leads/", include("apps.leads.urls")),
    path("", include("apps.deals.urls")),
    path("companies/", include("apps.companies.urls")),
    path("products/",include("apps.products.urls")),
    path("", include("apps.activities.urls")),
    path ("tickets/",include("apps.tickets.urls")),
    path("emails/", include("apps.emailactivity.urls")),
    path("calls/",include("apps.callActivity.urls"))
]
