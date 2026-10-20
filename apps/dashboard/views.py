from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.services.dashboard_service import (
    get_dashboard_stat_cards,
    get_dashboard_conversion_data,
    get_monthly_sales_report,
    get_yearly_sales_report,
    get_team_performance_data,
)


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        period = request.query_params.get("period", "monthly").lower()

        if period not in ["monthly", "yearly"]:
            return Response(
                {"error": "Invalid period. Use monthly or yearly."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        summary = get_dashboard_stat_cards()
        conversion = get_dashboard_conversion_data()
        team_performance = get_team_performance_data()

        if period == "yearly":
            sales_reports = get_yearly_sales_report()
        else:
            sales_reports = get_monthly_sales_report()

        return Response({
            "summary": summary,
            "conversion": conversion,
            "sales_reports": sales_reports,
            "team_performance": team_performance,
        })