from django.db import models
from organizations.models import Organization
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError




# Create your models here.
class Supplier(models.Model):
  STATUS_CHOICES=(
    ("ACTIVE","Active"),
    ("INACTIVE","Inactive"),
        )

  organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name="suppliers")
  supplier_code=models.CharField(max_length=50)
  name=models.CharField(max_length=150)
  phone=models.CharField(max_length=20)
  email=models.EmailField(blank=True,null=True)
  address=models.TextField(blank=True,null=True)
  status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="ACTIVE")
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)

  class Meta:
    unique_together=[
        "organization",
        "supplier_code"
    ]
  def __str__(self):
     return self.name
  
class Product(models.Model):  
  CATEGORY_CHOICES=(
    ("TABLET","Tablet"),
    ("CAPSULE","Capsule"),
    ("SYRUP","Syrup"),
    ("INJECTION","Injection"),
    ("CREAM","Cream"),
    ("DROPS","Drops"),
    ("OINTMENT","Ointment"),
  )
  STATUS_CHOICES=(
    ("ACTIVE","Active"),
    ("INACTIVE","Inactive"),
  )
  organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name="products")
  supplier=models.ForeignKey(Supplier,on_delete=models.CASCADE)
  product_code=models.CharField(max_length=50)
  barcode = models.CharField(max_length=50,unique=True,db_index=True,null=True,blank=True,help_text="Barcode used for POS scanning")
  name=models.CharField(max_length=150)
  generic_name=models.CharField(max_length=150,blank=True,null=True)
  category=models.CharField(max_length=50,choices=CATEGORY_CHOICES)
  purchase_price=models.DecimalField(max_digits=10,decimal_places=2)
  selling_price=models.DecimalField(max_digits=10,decimal_places=2)
  stock=models.IntegerField(default=0)
  minimum_stock=models.IntegerField(default=10)
  batch_number=models.CharField(max_length=100)
  expiry_date=models.DateField()
  manufacturer=models.CharField(max_length=150,blank=True,null=True)
  status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="ACTIVE")
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)

  class Meta:

    unique_together=[
      "organization",
      "product_code"
    ]
  def __str__(self):
     return self.name


class StockIn(models.Model):
      organization = models.ForeignKey(Organization,on_delete=models.CASCADE,related_name="stock_ins")
      product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="stock_entries")
      supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE,related_name="stock_ins")
      quantity=models.PositiveIntegerField()
      purchase_price=models.DecimalField(max_digits=10,decimal_places=2)
      batch_number=models.CharField(max_length=100)
      expiry_date=models.DateField()
      created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
      date=models.DateTimeField(default=timezone.now)
      created_at=models.DateTimeField(auto_now_add=True)
      def save(self,*args,**kwargs):
         #check new stock entry only
         if not  self.pk:
            self.product.stock+=self.quantity

            self.product.save()
         super().save(*args,**kwargs)

      def __str__(self):
         return f"{self.product.name} - {self.quantity}"      
      

class StockOut(models.Model):
   REASON_CHOICES=(
      ("SALE","Sale"),
      ("DAMAGED","Damaged"),
      ("Expired","Expired"),
      ("RETURNED","Returned"),
      ("OTHER","Other")
   )
   organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name="stock_outs")
   product=models.ForeignKey(Product,on_delete=models.CASCADE)
   quantity=models.PositiveIntegerField()
   reason=models.CharField(max_length=20,choices=REASON_CHOICES)
   remarks=models.TextField(blank=True,null=True)
   created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
   date=models.DateTimeField(default=timezone.now)
   created_at=models.DateTimeField(auto_now_add=True)

   def save(self,*args,**kwargs):
      
      if not self.pk:
         
         if self.qunatity>self.product.stock:
            raise ValidationError("Insufficent stock available.")
         
         self.product.stock-=self.qunatity
         self.product.save()
      super().save(*args,**kwargs)

   def __str__(self):
      return  f"{self.product.name} ({self.quantity})"
      