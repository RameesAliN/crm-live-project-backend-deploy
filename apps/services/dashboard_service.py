from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import ExtractMonth
from django.db.models.functions import ExtractYear

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
def get_dashboard_stat_cards():
    summary = get_dashboard_summary()

    return [
        {
            "title": "Total Leads",
            "value": f"{summary['total_leads']:,}",
            "icon": "Users",
            "iconBackground": "bg-gradient-to-b from-[#b9afff] to-white",
            "iconColor": "text-[#5946e8]",
        },
        {
            "title": "Active Deals",
            "value": f"{summary['active_deals']:,}",
            "icon": "BriefcaseBusiness",
            "iconBackground": "bg-gradient-to-b from-[#9ce8da] to-white",
            "iconColor": "text-[#20c7a7]",
        },
        {
            "title": "Closed Deals",
            "value": f"{summary['closed_deals']:,}",
            "icon": "BriefcaseBusiness",
            "iconBackground": "bg-gradient-to-b from-[#ffc1c5] to-white",
            "iconColor": "text-[#ff7c85]",
        },
        {
            "title": "Monthly Revenue",
            "value": f"{summary['monthly_revenue']:,.0f}",
            "icon": "Banknote",
            "iconBackground": "bg-gradient-to-b from-[#f6d278] to-white",
            "iconColor": "text-[#e4a500]",
        },
    ]



def get_dashboard_conversion():
    return {
        "contact": Lead.objects.count(),
        "qualified_lead": Lead.objects.filter(lead_status="Qualified").count(),
        "proposal_sent": Deal.objects.filter(stage="proposal_sent").count(),
        "negotiation": Deal.objects.filter(stage="negotiation").count(),
        "closed_won": Deal.objects.filter(stage="closed_won").count(),
        "closed_lost": Deal.objects.filter(stage="closed_lost").count(),
    }
def get_dashboard_conversion_data():
    conversion = get_dashboard_conversion()

    stages = [
        ("Contact", "contact", "bg-[#5b49e5]"),
        ("Qualified Lead", "qualified_lead", "bg-[#2ecdb8]"),
        ("Proposal Sent", "proposal_sent", "bg-[#ffc400]"),
        ("Negotiation", "negotiation", "bg-[#6670df]"),
        ("Closed Won", "closed_won", "bg-[#10d46c]"),
        ("Closed Lost", "closed_lost", "bg-[#ff4d4f]"),
    ]
    max_count = max(conversion.values(), default=0)

    return [
        {
            "label": label,
            "width": f"{round(count / max_count * 100)}%" if max_count else "0%",
            "color": color,
        }
        for label, key, color in stages
        for count in [conversion[key]]
    ]



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

    revenue_by_month = {
        item["month"]: item["total_revenue"]
        for item in sales
    }

    months = [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec",
    ]

    return [
        {
            "month": month_name,
            "solid": float(
                revenue_by_month.get(month_number, 0)
            ),
        }
        for month_number, month_name in enumerate(
            months, start=1
        )
    ]
def get_yearly_sales_report():
    sales = (
        Deal.objects.filter(
            stage="closed_won"
        )
        .annotate(year=ExtractYear("close_date"))
        .values("year")
        .annotate(total_revenue=Sum("amount"))
        .order_by("year")
    )

    return [
        {
            "year": item["year"],
            "solid": float(item["total_revenue"] or 0),
        }
        for item in sales
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
def get_team_performance_data():
    performance = get_team_performance()

    return [
        {
            "employee": item["employee_name"],
            "activeDeals": item["active_deals"],
            "closedDeals": item["closed_deals"],
            "revenue": f"${item['revenue']:,.0f}",
            "change": (
                f"{item['revenue_growth_percentage']:+.1f}%"
                if item["revenue_growth_percentage"] is not None
                else "N/A"
            ),
            "positive": (
                item["revenue_growth_percentage"] >= 0
                if item["revenue_growth_percentage"] is not None
                else False
            ),
        }
        for item in performance
    ]