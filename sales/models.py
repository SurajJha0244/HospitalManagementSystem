from django.db import models
from django.conf import settings

from organizations.models import Organization
from inventory.models import Product


class Customer(models.Model):

    organization = models.ForeignKey(Organization,on_delete=models.CASCADE,related_name="customers")
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20,blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Sale(models.Model):


    PAYMENT_CHOICES = (
        ("CASH", "Cash"),
        ("CARD", "Card"),
        ("ONLINE", "Online"),
    )


    organization = models.ForeignKey(Organization,on_delete=models.CASCADE,related_name="sales")
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True,related_name="sales")
    invoice_number = models.CharField(max_length=50,unique=True)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    discount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    tax = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    total = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    payment_method = models.CharField(max_length=20,choices=PAYMENT_CHOICES,default="CASH")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name="sales_created")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):

        return self.invoice_number



class SaleItem(models.Model):


    sale = models.ForeignKey(Sale,related_name="items",on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.PROTECT,related_name="sale_items")
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2,default=0)


    def save(self, *args, **kwargs):

        self.subtotal = (
            self.quantity *
            self.price
        )

        super().save(*args, **kwargs)


    def __str__(self):

        return f"{self.product.name} x {self.quantity}"




class Payment(models.Model):


    PAYMENT_METHODS = (
        ("CASH", "Cash"),
        ("CARD", "Card"),
        ("ONLINE", "Online"),
    )


    sale = models.ForeignKey(Sale,on_delete=models.CASCADE,related_name="payments")
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    method = models.CharField(max_length=20,choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20,default="COMPLETED")
    transaction_id = models.CharField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return self.sale.invoice_number