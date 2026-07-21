from rest_framework import serializers
from .models import Supplier,Product,StockIn

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        fields=[
            "id",
            "supplier_code",
            "name",
            "phone",
            "email",
            "address",
            "status",
            "created_at",
            "updated_at"

        ]
        read_only_fields=["created_at","updated_at"]

class ProductSerializer(serializers.ModelSerializer):
    supplier_name=serializers.CharField(source="supplier.name",read_only=True)

    class Meta:
        model=Product
        fields=[
                        "id",

            "product_code",

            "name",

            "generic_name",

            "category",

            "supplier",

            "supplier_name",

            "purchase_price",

            "selling_price",

            "stock",

            "minimum_stock",

            "batch_number",

            "expiry_date",

            "manufacturer",

            "status",

            "created_at",

            "updated_at"

        ]
        read_only_fields=[
            "stock",
            "created_at",
            "updated_at"
        ]

class  StockInSerailizer(serializers.ModelSerializer):
    product_name=serializers.CharField(source="product.name",read_only=True)
    supplier_name=serializers.CharField(source="supplier.name",read_only=True)

    class Meta:
        model=StockIn  
        fields=[
            "id",

            "product",

            "product_name",

            "supplier",

            "supplier_name",

            "quantity",

            "purchase_price",

            "batch_number",

            "expiry_date",

            "created_by",

            "date",

            "created_at"

        ]    
        read_only_filed=[
             "created_by",
             "created_at",
             "date"
        ]