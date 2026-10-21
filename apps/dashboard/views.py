from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.services.dashboard_service import (
    get_dashboard_summary,
    get_dashboard_conversion,
    get_monthly_sales_report,
    get_team_performance,
)


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        summary = get_dashboard_summary()
        conversion = get_dashboard_conversion()
        sales_reports = get_monthly_sales_report()
        team_performance = get_team_performance()

        return Response({
            "summary": summary,
            "conversion": conversion,
            "sales_reports": sales_reports,
            "team_performance": team_performance,
        })