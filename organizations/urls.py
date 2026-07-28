from django.urls import path
from .views import (OrganizationListCreateAPIView,OrganizationDetailAPIView,OrganizationProfileAPIView)

urlpatterns=[
    path("profile/",OrganizationProfileAPIView.as_view(),name="organization-profile"),
    path("", OrganizationListCreateAPIView.as_view(),name="organizations"),
    path("<int:id>/",OrganizationDetailAPIView.as_view(),name="organization-detail"),
   
        
]

