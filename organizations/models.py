from django.db import models
import uuid

# Create your models here.
class Organization(models.Model):

    #Basic Infromation
    name=models.CharField(max_length=200)
    organization_id = models.CharField(max_length=20,unique=True,blank=True,null=True)
    established_date=models.DateField(blank=True,null=True)

    #Contact Infromation

    address=models.TextField(blank=True,null=True)
    phone=models.CharField(max_length=20,blank=True,null=True)
    email=models.EmailField(blank=True,null=True)

    #pharmacy Legal information
    registration_number= models.CharField(max_length=100,blank=True,null=True)
    license_number= models.CharField(max_length=100,blank=True,null=True)
    pan_number= models.CharField(max_length=100,blank=True,null=True)
    
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def save(self,*args,**kwargs):

        if not self.organization_id:
            self.organization_id=("ORG-"+str(uuid.uuid4().hex[:8].upper()))
        super().save(*args,**kwargs)    


    def __str__(self):
        return self.name