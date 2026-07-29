from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (LoginSerializer,UserSerializer)
from organizations.models import Organization
from .serializers import OrganizationAdminSerializer,StaffUserSerializer
from accounts.permissions import IsSuperAdmin
from accounts.permissions import IsSuperAdminOrOrganizationAdmin

from .models import User
from django.shortcuts import get_object_or_404
from .serializers import ChangePasswordSerializer



class LoginAPIView(APIView):

    permission_classes=[]
    def post(self,request):

        serializer=LoginSerializer(
            data=request.data
        )


        if serializer.is_valid():

            user=serializer.validated_data["user"]


            refresh=RefreshToken.for_user(user)


            return Response({

                "message":"Login successful",

                "access":str(refresh.access_token),

                "refresh":str(refresh),


                "user":UserSerializer(user).data
            })

                   
                

            


        return Response(

            serializer.errors,

            status=status.HTTP_400_BAD_REQUEST

        )
    

class ProfileAPIView(APIView):

    permission_classes=[
        IsAuthenticated
    ]

    def get(self,request):
        serializer=UserSerializer(
        request.user
        )
        return Response(serializer.data)
    
class LogoutAPIView(APIView):
    permission_classes=[ IsAuthenticated]    

    def post(self,request):
        try:
            refresh_token=request.data.get("refresh")

            token=RefreshToken(refresh_token)

            token.blacklist()

            return Response({"message":
                        "Logout sucessful"     })
        except Exception:

             return Response({"error":
                              "Invalid token"},status=400)


class CreateOrganizationAdminAPIView(APIView):
    permission_classes=[
        IsAuthenticated,
        IsSuperAdmin
    ]
        

    def post(self,request,organization_id):
        organization=Organization.objects.get(id=organization_id)  
        serializer=OrganizationAdminSerializer(data=request.data)
        if serializer.is_valid():
            user=User.objects.create_user(
                username=serializer.validated_data["username"],
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
                phone=serializer.validated_data["phone"],
                role=User.Role.ORGANIZATION_ADMIN,
                organization=organization

            ) 

            return Response({
                "message":"Organization Admin Created",
                "username":user.username,
                "organization":organization.name
            })
        
        return Response(serializer.errors,status=400)

class CreateStaffAPIView(APIView):

    permission_classes=[
        IsAuthenticated,
        IsSuperAdminOrOrganizationAdmin
    ]    

    def post(self,request):
        serializer=StaffUserSerializer(data=request.data)

        if serializer.is_valid():
              role=serializer.validated_data["role"]
              if role==User.Role.SUPER_ADMIN:
                  return Response({"error":"Invalid Role"},status=400)

              if role==User.Role.ORGANIZATION_ADMIN:
                   return Response({"error":"Invalid Role"},status=400)

              user=User.objects.create_user(
              username=serializer.validated_data["username"],
              email=serializer.validated_data["email"],
              password=serializer.validated_data["password"],
              phone=serializer.validated_data["phone"],
              role=role,
              organization=request.user.organization
        )    
              return Response({"message":"Staff Created",
                         "username":user.username}) 
        
        return Response(serializer.errors,status=400)

class OrganizationUserListAPIView(APIView):

    permission_classes=[
        IsAuthenticated,
        IsSuperAdminOrOrganizationAdmin
    ]

    def get(self,request):
        user=request.user

        if user.role==User.Role.SUPER_ADMIN:
            users=User.objects.all()

        else:

            users=User.objects.filter(organization=user.organization).exclude(role=User.Role.ORGANIZATION_ADMIN)  

        serializer =UserSerializer(users,many=True)   


        return Response(serializer.data)  

class OrganizationUserDetailAPIView(APIView):

    permission_classes=[
        IsAuthenticated,
        IsSuperAdminOrOrganizationAdmin
    ]

    def get_object(self,request,id):

        if request.user.role==User.Role.SUPER_ADMIN:

            return get_object_or_404(User,id=id)
        

        return get_object_or_404(User,id=id,organization=request.user.organization)
    
    def get(self,request,id):
        user=self.get_object(request,id)
        serializer=UserSerializer(user)
        return Response (serializer.data)
    
    def put(self,request,id):
        user=self.get_object(request,id)
        serializer=UserSerializer(user,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)
    def delete(self,request,id):
        user=self.get_object(request,id)
        user.delete()

        return Response({"message":"User deleted sucessfully"})



class ChangePasswordAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer=ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=request.user

        if not user.check_password(
            serializer.validated_data["old_password"]):

            return Response({
                "old_password":["Current password is incorrect."]
            },status=status.HTTP_400_BAD_REQUEST)


        user.set_password(serializer.validated_data["new_password"])

        user.save()

        return Response(
            {
                "message":"Password changed sucessfully"
            }
        )

     
class UserProfileAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    # view own profile 

    def get(self,request):

        serializer = UserProfileSerializer(
            request.user
        )

        return Response(
            serializer.data
        )

        #update own profile

        def put(self ,request):

            serializer = UserProfileSerializer(
                request.user,
                data=request.data,
                partial=True
            )

            serializer.is_valid(
                raise_exception=True
            )

            serializer.save()

            return Response(
                serializer.data
            )

