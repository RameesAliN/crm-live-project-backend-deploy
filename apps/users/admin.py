from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
    "email",
    "first_name",
    "last_name",
    "role",
    "is_active",
    "requested_role",
    "role_approved",
    "is_staff",
    )

    list_filter = (
    "role",
    "requested_role",
    "role_approved",
    "is_staff",
    "is_active",)
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    readonly_fields = (
    "role",
    "requested_role",
    "role_approved",
)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Information", {
            "fields": (
                "first_name",
                "last_name",
                "phone",
                "company_name",
                "industry_type",
                "country",)}),
        ("CRM Role", {"fields": (
        "role",
        "requested_role",
        "role_approved",)}),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )}),
        ("Important Dates", {
            "fields": ("last_login", "date_joined")}),)

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "usable_password", "password1", "password2"),
        }),)
    
    actions = ["approve_requested_role"]
    def get_actions(self, request):
        actions = super().get_actions(request)

        if not request.user.is_superuser:
            actions.pop("approve_requested_role", None)

        return actions

    @admin.action(description="Approve selected users' requested roles")
    def approve_requested_role(self, request, queryset):

        if not request.user.is_superuser:
            self.message_user(
                request,
                "Only Super Admin can approve roles.",
                level="error"
            )
            return

        approved_count = 0

        for user in queryset:
            if user.is_superuser:
                continue

            if user.role_approved and user.role == user.requested_role:
                 continue

            user.role = user.requested_role
            user.role_approved = True
            user.save(update_fields=["role", "role_approved"])

            approved_count += 1

        self.message_user(
            request,
            f"{approved_count} user(s) approved successfully."
        )
    