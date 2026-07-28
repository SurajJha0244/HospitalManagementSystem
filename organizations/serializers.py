from rest_framework import serializers
from .models import Organization

class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model=Organization

        fields=[

            "id",
            "organization_id",
            "name",
            "address",
            "phone",
            "established_date",
            "registration_number",
            "license_number",
            "pan_number",
            "email",
            "is_active",
            "created_at",
            "updated_at",

        ]

        read_only_fields=[
            "organization_id",
            "created_at",
            "updated_at"

        ]