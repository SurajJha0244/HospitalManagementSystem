from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from django.contrib.auth.hashers import make_password



class LoginSerializer(serializers.Serializer):

    username=serializers.CharField()

    password=serializers.CharField(write_only=True)

    def validate(self,data):
        username=data.get("username")
        password=data.get("password")


        user=authenticate(
            username=username,
            password=password
        )

        if user is None:
            raise serializers.ValidationError("Invalid username or password")
        

        if not user.is_active:
            raise serializers.ValidationError(
                "user account disabled "
            )
        
        if (
            user.role!=User.Role.SUPER_ADMIN
            and user.organization is None
        ):
            raise serializers.ValidationError("user is not assigned to any organization")
        
        if (
            user.role!=User.Role.SUPER_ADMIN
            and not user.organization.is_active
        ):
            raise serializers.ValidationError("Organaaization is inactive")

        data["user"]=user

        return data
    
class UserSerializer(serializers.ModelSerializer):
    organization_name=serializers.CharField(source="organization.name",read_only=True)

    class Meta:
        model=User
        fields=[
            "id",
            "username",
            "email",
            "phone",
            "role",
            "organization_name"
        ]

    def get__organization_name(self,obj):

        if obj.organization:
            return obj.organization.name

        return None    
    
class UserCreateSerializer(serializers.ModelSerializer):  
    password=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=[
            "id",
            "username",
            "email",
            "password",
            "phone",
            "role",
            "organization"
        ]  
    def create (self,validated_data):
            validated_data["password"]=make_password(validated_data["password"])

            return User.objects.create(**validated_data)
    
class OrganizationAdminSerializer(serializers.ModelSerializer):
        password=serializers.CharField(write_only=True)

        class Meta:
            model=User

            fields=[
                "username",
                "email",
                "password",
                "phone"
            ]

class StaffUserSerializer(serializers.ModelSerializer):
     password=serializers.CharField(write_only=True)

     class Meta:
          model=User
          fields=[
               "username",
               "email",
               "password",
               "phone",
               "role"
          ]

class UserProfileSerializer(serializers.ModelSerializer):

    organization = serializers.CharField(source="organization.name",read_only=True)

    class Meta:
       model = User
       fields = [
           "username","first_name","last_name","email","phone","role","organization",
       ]

       read_only_fields = [
        "username",
        "role",
        "organization",
       ]