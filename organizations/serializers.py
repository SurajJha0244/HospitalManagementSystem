from rest_framework import serializers
from .models import Organization

class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model=Organization

        fields=[

            "id",
            "organization_id",
            "name",
            "name",
            "address",
            "phone",
            "email",
            "is_active",
            "created_at"

        ]

        read_only_fields=[
            "organization_id",
            "created_at"
        ]