from django.db import models
from django.contrib.auth.models import AbstractUser
from organizations.models import Organization

# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN="SUPER_ADMIN","Super Admin"
        ORGANIZATION_ADMIN="ORGANIZATION_ADMIN","Organization Admin"
        PHARMACIST="PHARMACIST","Pharmacist"
        CASHIER="CASHIER","Cashier"
        STAFF="STAFF","Staff"
    
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,null=True,blank=True,related_name="users")
    role=models.CharField(max_length=30,choices=Role.choices,default=Role.STAFF)

    phone=models.CharField(max_length=20,blank=True,null=True)



    def save(self, *args, **kwargs):

        if self.role != self.Role.SUPER_ADMIN and not self.organization:

            raise ValueError(
                "Only Super Admin can have no organization"
            )

        super().save(*args, **kwargs)
        


    def __str__(self):
        return f"{self.username}{self.role}"  
    
