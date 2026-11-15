
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = (
        "name",
        "mobile_number",
        "is_approved",
        "is_active",
        "is_staff",
    )

    list_filter = (
        "is_approved",
        "is_active",
        "is_staff",
    )

    search_fields = (
        "name",
        "mobile_number",
    )

    ordering = ("mobile_number",)

    actions = [
        "approve_users",
        "deactivate_users",
    ]

    @admin.action(description="Approve selected users")
    def approve_users(self, request, queryset):
        queryset.update(is_approved=True, is_active=True)

    @admin.action(description="Deactivate selected users")
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)

    fieldsets = (
        ("User Information", {
            "fields": (
                "name",
                "mobile_number",
                "password",
            )
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_approved",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important Dates", {
            "fields": (
                "last_login",
                "date_joined",
            )
        }),
    )

    add_fieldsets = (
        ("Create User", {
            "classes": ("wide",),
            "fields": (
                "name",
                "mobile_number",
                "password1",
                "password2",
                "is_active",
                "is_approved",
                "is_staff",
            ),
        }),
    )

    filter_horizontal = (
        "groups",
        "user_permissions",
    )
