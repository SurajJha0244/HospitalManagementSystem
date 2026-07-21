from django.urls import path
from .views import (OrganizationListCreateAPIView,OrganizationDetailAPIView)

urlpatterns=[
    path("", OrganizationListCreateAPIView.as_view(),name="organizations"),
    path("<int:id>/",OrganizationDetailAPIView.as_view(),name="organization-detail")
        
]

