from django.contrib import admin
from .models import Supplier,Product,StockIn
# Register your models here.
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display=["supplier_code","name","email","status","organization"]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=[
        "product_code",
        "name",
        "category",
        "selling_price",
        "stock",
        "expiry_date",
        "organization"
    ]
    search_fields=[
        "name",
        "product_code"
    ]

@admin.register(StockIn)
class StockInAdmin(admin.ModelAdmin):
    list_display=[
        "product",
        "supplier",
        "quantity",
        "purchase_price",
        "expiry_date",
        "created_at",
        "batch_number",
        "date"
        

    ]    