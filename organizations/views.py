from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Organization
from .serializers import OrganizationSerializer

from accounts.permissions import (
    IsSuperAdmin,
    IsOrganizationAdmin
)



class OrganizationListCreateAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin
    ]


    # Get all organizations
    def get(self, request):

        organizations = Organization.objects.all()

        serializer = OrganizationSerializer(
            organizations,
            many=True
        )

        return Response(
            serializer.data
        )


    # Create organization
    def post(self, request):

        serializer = OrganizationSerializer(
            data=request.data
        )


        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )


        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class OrganizationDetailAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsSuperAdmin
    ]


    # Get single organization
    def get(self, request, id):

        organization = get_object_or_404(
            Organization,
            id=id
        )

        serializer = OrganizationSerializer(
            organization
        )

        return Response(
            serializer.data
        )


    # Update organization
    def put(self, request, id):

        organization = get_object_or_404(
            Organization,
            id=id
        )

        serializer = OrganizationSerializer(
            organization,
            data=request.data
        )


        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )


        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


    # Delete organization
    def delete(self, request, id):

        organization = get_object_or_404(
            Organization,
            id=id
        )

        organization.delete()

        return Response(
            {
                "message": "organization deleted successfully"
            },
            status=status.HTTP_200_OK
        )



class OrganizationProfileAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsOrganizationAdmin
    ]


    # Organization admin view own profile
    def get(self, request):

        organization = request.user.organization

        serializer = OrganizationSerializer(
            organization
        )

        return Response(
            serializer.data
        )


    # Full update profile
    def put(self, request):

        organization = request.user.organization

        serializer = OrganizationSerializer(
            organization,
            data=request.data
        )


        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )


        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


    # Partial update profile
    def patch(self, request):

        organization = request.user.organization

        serializer = OrganizationSerializer(
            organization,
            data=request.data,
            partial=True
        )


        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )


        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )