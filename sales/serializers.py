from rest_framework import serializers
from .models import Customer,Sale,SaleItem
from inventory import Product


class CustomerSerializer(serializers.Modelserializer):
    class Meta:

        model = Customer

        fields = [
            "id",
            "name",
            "phone",
            "address",
            "created_at",
        ]

        read_only_fields = [
            "created_at",
        ]


class SaleItemSerializer(serializers.Modelserializer):
   
   product_name = serializers.CharField(source="product.name",read_only=True)
   barcode = serializers.CharField(source="product.barcode",read_only=True)

   class Meta:

      model = SaleItem

      fields=["id", "product", "product_name", "barcode", "quantity", "subtotal",  "price",]
      read_only_fields = [
        "subtotal",
      ]

class SaleSerializer(serializers.Modelserializer):

   item = SaleItemSerializer(many=True,read_only=True)
   customer_name = serializers.CharField(source="customer.name",read_only_field=True)

   class Meta:
      model = Sale
      fields=["id","invoice_number","customer","customer_name","subtotal","discount","tax","total","payment_method","create_by","created_at","items"]

      read_only_fields = [
        "invoice_number",
        "subtotal",
        "tax",
        "total",
        "created_by",
        "created_at",
      ]

class CreateSaleSerializer(serializers.Serializer):
   customer_name = serializers.CharField(max_length=100,required=False,allow_blank=True)
   payment_method = serializers.CharField(
    choices = [
        "CASH",
        "CARD",
        "ONLINE",
    ]
   )
   discount = serializers.DecimalField(max_digit=10,decimal_places=2,required=False,default=0)


   Items=CreateSaleItemSerializer(
    many=True
   )


   
   






 










   class Meta:
      
        model = Sale

        fields = [

        ]
