from rest_framework import serializers
from .models import Customer,Sale,SaleItem
from inventory.models import Product



class CustomerSerializer(serializers.ModelSerializer):
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


class SaleItemSerializer(serializers.Serializer):
   
   product_name = serializers.CharField(source="product.name",read_only=True)
   barcode = serializers.CharField(source="product.barcode",read_only=True)

   class Meta:

      model = SaleItem

      fields=[
            "id",

            "product",

            "barcode",

            "product_code",

            "product_name",

            "batch_number",

            "expiry_date",

            "quantity",

            "unit_price",

            "discount",

            "tax",

            "subtotal"

      ]
      read_only_fields = [
        "subtotal",
      ]

class SaleSerializer(serializers.ModelSerializer):

   item = SaleItemSerializer(many=True,read_only=True)
   customer_name = serializers.CharField(source="customer.name",read_only=True)

   class Meta:
      model = Sale
      fields=["id","invoice_number","customer","customer_name","subtotal","discount","tax","total","payment_method","created_by","created_at","items"]

      read_only_fields = [
        "invoice_number",
        "subtotal",
        "tax",
        "total",
        "created_by",
        "created_at",
      ]

class CreateSaleItemSerializer(serializers.ModelSerializer):


    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )


    quantity = serializers.IntegerField(
        min_value=1
    )


    discount = serializers.DecimalField(

        max_digits=12,

        decimal_places=2,

        required=False,

        default=0

    )



class CreateSaleSerializer(serializers.ModelSerializer):
   customer_name = serializers.CharField(max_length=100,required=False,allow_blank=True)
   payment_method = serializers.ChoiceField(
    choices = [
        "CASH",
        "CARD",
        "FONEPAY",
        "ESEWA",
        "BANK TRANSFER",

    ]
   )
   discount = serializers.DecimalField(max_digits=10,decimal_places=2,required=False,default=0)


   Items=CreateSaleItemSerializer(
    many=True
   )




   
   
