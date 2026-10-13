from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import ( # type: ignore
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # User APIs
    path("api/", include("apps.users.urls")),
    path("api/leads/", include("apps.leads.urls")),

    # Swagger Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]