from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import ExtractMonth

from apps.leads.models import Lead
from apps.deals.models import Deal
from django.contrib.auth import get_user_model


def get_dashboard_summary():
    today = timezone.localdate()

    total_leads = Lead.objects.count()

    active_deals = Deal.objects.filter(stage__in=["proposal_sent", "negotiation"]).count()

    closed_deals = Deal.objects.filter(stage__in=["closed_won", "closed_lost"]).count()

    monthly_revenue = Deal.objects.filter(
        stage="closed_won",
        close_date__year=today.year,
        close_date__month=today.month,
    ).aggregate(total=Sum("amount"))["total"] or 0

    return {
        "total_leads": total_leads,
        "active_deals": active_deals,
        "closed_deals": closed_deals,
        "monthly_revenue": monthly_revenue,
    }



def get_dashboard_conversion():
    return {
        "contact": Lead.objects.count(),
        "qualified_lead": Lead.objects.filter(lead_status="Qualified").count(),
        "proposal_sent": Deal.objects.filter(stage="proposal_sent").count(),
        "negotiation": Deal.objects.filter(stage="negotiation").count(),
        "closed_won": Deal.objects.filter(stage="closed_won").count(),
        "closed_lost": Deal.objects.filter(stage="closed_lost").count(),
    }



def get_monthly_sales_report():
    current_year = timezone.localdate().year

    sales = (
        Deal.objects.filter(
            stage="closed_won",
            close_date__year=current_year,
        )
        .annotate(month=ExtractMonth("close_date"))
        .values("month")
        .annotate(total_revenue=Sum("amount"))
        .order_by("month")
    )

    revenue_by_month = { item["month"]: item["total_revenue"] for item in sales}

    months = [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec",
    ]

    return [
        {
            "month": month_name,
            "revenue": revenue_by_month.get(month_number, 0),
        }
        for month_number, month_name in enumerate(months, start=1)
    ]



def get_team_performance():
    User = get_user_model()

    today = timezone.localdate()

    current_month_start = today.replace(day=1)

    previous_month_end = current_month_start - timedelta(days=1)
    previous_month_start = previous_month_end.replace(day=1)

    employees = User.objects.filter(is_active=True)

    performance = []

    for employee in employees:
        deals = Deal.objects.filter(owners=employee)

        active_deals = deals.filter(
            stage__in=["proposal_sent", "negotiation"]
        ).count()

        closed_deals = deals.filter(
            stage__in=["closed_won", "closed_lost"]
        ).count()

        current_revenue = deals.filter(
            stage="closed_won",
            close_date__gte=current_month_start,
            close_date__lte=today,
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0

        previous_revenue = deals.filter(
            stage="closed_won",
            close_date__gte=previous_month_start,
            close_date__lte=previous_month_end,
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0

        if previous_revenue > 0:
            growth_percentage = round(
                (current_revenue - previous_revenue)
                / previous_revenue * 100,
                2,
            )
        else:
            growth_percentage = None

        performance.append({
            "employee_id": employee.id,
            "employee_name": employee.get_full_name() or employee.email,
            "active_deals": active_deals,
            "closed_deals": closed_deals,
            "revenue": current_revenue,
            "revenue_growth_percentage": growth_percentage,
        })

    return performance