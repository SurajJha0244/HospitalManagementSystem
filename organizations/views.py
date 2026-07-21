from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .models import Organization
from .serializers import OrganizationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.permissions import IsSuperAdmin

# Create your views here.
class OrganizationListCreateAPIView(APIView):

    permission_classes=[
        IsAuthenticated,
        IsSuperAdmin
    ]


    def get(self,reqquest):
       organizations=Organization.objects.all()
       serializer=OrganizationSerializer(organizations,many=True)
       return Response(serializer.data)


    def post(self,request):
        serializer=OrganizationSerializer(data=request.data)


        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=400)
    
class OrganizationDetailAPIView(APIView):

    permission_classes=[
        IsAuthenticated,
        IsSuperAdmin
    ]    

    def get(self,reqquest,id):

        organization =Organization.objects.get(id=id)
        serializer=OrganizationSerializer(organization)
        return Response(serializer.data)
    
    def put(self,request,id):
        organization=Organization.objects.get(id=id)
        serializer=OrganizationSerializer(organization,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors,status=400)
    
    def delete(self,request,id):
        organization=Organization.objects.get(id=id)
        organization.delete()

        return Response({"message":"organization deleted"})
