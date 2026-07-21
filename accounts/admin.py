from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    model = User

    list_display = (
        "username",
        "email",
        "organization",
        "role",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "organization",
        "role",
        "is_staff",
        "is_active",
    )


    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "organization",
                    "role",
                    "phone",
                )
            },
        ),
    )


    add_fieldsets = (
        (
            None,
            {
                "classes": (
                    "wide",
                ),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "organization",
                    "role",
                    "phone",
                ),
            },
        ),
    )