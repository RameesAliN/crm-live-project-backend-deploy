
from django.urls import path, include

urlpatterns = [
    path("", include("apps.users.urls")),
    path("leads/", include("apps.leads.urls")),
    path("", include("apps.deals.urls")),
    path("companies/", include("apps.companies.urls")),
    path("products/",include("apps.products.urls")),
    path("notes/", include("apps.activities.urls")),
    path("", include("apps.emailactivity.urls"))
    path ("tickets/",include("apps.tickets.urls"))
]
