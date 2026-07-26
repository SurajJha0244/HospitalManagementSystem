from rest_framework.permissions import BasePermission

from .models import User



# Only Super Admin can access
class IsSuperAdmin(BasePermission):

    def has_permission(self, request, view):

        return (

            request.user.is_authenticated

            and

            request.user.role == User.Role.SUPER_ADMIN

        )



# Only Organization Admin can access
class IsOrganizationAdmin(BasePermission):

    def has_permission(self, request, view):

        return (

            request.user.is_authenticated

            and

            request.user.role == User.Role.ORGANIZATION_ADMIN

        )



# Super Admin OR Organization Admin can access
class IsSuperAdminOrOrganizationAdmin(BasePermission):

    def has_permission(self, request, view):

        return (

            request.user.is_authenticated

            and

            request.user.role in [

                User.Role.SUPER_ADMIN,

                User.Role.ORGANIZATION_ADMIN

            ]

        )