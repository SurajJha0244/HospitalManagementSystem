from django.urls import path
from .views import ( LoginAPIView,ProfileAPIView,LogoutAPIView)
from rest_framework_simplejwt.views import(TokenRefreshView)
from .views import (CreateOrganizationAdminAPIView,CreateStaffAPIView)
from .views import (OrganizationUserListAPIView,OrganizationUserDetailAPIView)

urlpatterns = [ 
    path("login/",LoginAPIView.as_view(),name="login"),
    path( "profile/",ProfileAPIView.as_view(),name="profile"),
    path("logout/",LogoutAPIView.as_view(), name="logout" ),
    path( "token/refresh/", TokenRefreshView.as_view(), name="token_refresh" ),
    path("organization/<int:organization_id>/admin/",CreateOrganizationAdminAPIView.as_view()),
    path("staff/create/",CreateStaffAPIView.as_view()),
    path("users/",OrganizationUserListAPIView.as_view(),name="organization-users"),
    path("users/<int:id>/", OrganizationUserDetailAPIView.as_view(),name="organization-user-detail"),

]
