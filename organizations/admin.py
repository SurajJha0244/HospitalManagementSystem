from django.contrib import admin
from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "organization_id",
        "phone",
        "email",
        "is_active",
        "created_at"
    ]

    search_fields = [
        "name",
        "organization_id"
    ]