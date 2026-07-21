from rest_framework.permissions import BasePermission
from .models import User



class IsSuperAdmin(BasePermission):


    def has_permission(
        self,
        request,
        view
    ):


        return (

            request.user.is_authenticated

            and

            request.user.role=="SUPER_ADMIN"

        )
    
class IsSuperAdminOrOrganizationAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenicated and request.user.role in [User.Role.SUPER_ADMIN,User.Role.ORGANIZATION_ADMIN] )   