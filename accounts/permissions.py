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

<<<<<<< HEAD
<<<<<<< HEAD
=======
        )

=======
>>>>>>> 00fd26aee58aabaa7df6a3c7d240e91c3c059d73
# Only Pharmacist
class IsPharmacist(BasePermission):

    def has_permission(self, request, view):

        return (

            request.user.is_authenticated

            and

            request.user.role == User.Role.PHARMACIST

        )



# Only Cashier
class IsCashier(BasePermission):

    def has_permission(self, request, view):

        return (

            request.user.is_authenticated

            and

            request.user.role == User.Role.CASHIER

        )



# Only Staff
class IsStaff(BasePermission):

    def has_permission(self, request, view):

        return (

            request.user.is_authenticated

            and

            request.user.role == User.Role.STAFF

        )



# Users who can manage other users
class CanManageUsers(BasePermission):

    def has_permission(self, request, view):

        return (

            request.user.is_authenticated

            and

            request.user.role in [

                User.Role.SUPER_ADMIN,

                User.Role.ORGANIZATION_ADMIN

            ]
<<<<<<< HEAD

>>>>>>> 34afa3d9007df5222a391197710bff38719b08a4
=======
>>>>>>> 00fd26aee58aabaa7df6a3c7d240e91c3c059d73
        )