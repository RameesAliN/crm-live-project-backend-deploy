
from django.urls import path, include

urlpatterns = [
    path("", include("apps.users.urls")),
    path("leads/", include("apps.leads.urls")),
    path("", include("apps.deals.urls")),
    path("products/",include("apps.products.urls")),
    path("companies/", include("apps.companies.urls"))
    
]
