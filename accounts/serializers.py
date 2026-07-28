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
    organization_name=serializers.SerializerMethodField()

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

    def get_organization_name(self,obj):

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
            user = User.objects.create_user(

            username=validated_data["username"],

            email=validated_data.get("email"),

            password=validated_data["password"],

            phone=validated_data.get("phone"),

            role=validated_data.get(
                "role",
                User.Role.STAFF
            )

        )

            return user
    
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
          def create(self,validated_data):

                    return User.objects.create_user(**validated_data)

          read_only_fields=("role")


class ChangePasswordSerializer(serializers.Serializer):
     old_password=serializers.CharField(write_only=True)
     new_password=serializers.CharField(write_only=True)
     confirm_password=serializers.CharField(write_only=True)

     def validate(self,attrs):

          if attrs["new_password"]!=attrs["confirm_password"]:
               raise serializers.ValidationError(
                    {
                         "confirm_password":"Password do not match."
                    }
               )
          return attrs
