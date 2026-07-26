from django.shortcuts import render
from decimal import Decimal
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import (Customer,Sale,SaleItem)
from .serializers import (SaleSerializer,CreateSaleSerializer)
from inventory.models import Product
from inventory.serializers import ProductBarcodeSerializer
from rest_framework.permissions import IsAuthenticated




def generate_invoice_number():

    last_sale=Sale.objects.order_by("-id").first()

    if last_sale:
        number=last_sale.id+1
    else:
        number=1

    return f"INV-{number:06d}"
# Create your views here.
class ProductBarcodeAPIView(APIView):
    def get(self,request,barcode):
        product=get_object_or_404(Product,barcode=barcode,organization=request.user.organization)

        data={
            "id":product.id,
            "barcode":product.barcode,
            "product_code":product.product_code,
            "name": product.name,
            "selling_price": product.selling_price,
            "stock": product.stock_quantity,

        }
        return Response(data)


class CreateSaleAPIView(APIView):   

    @transaction.atomic 
    def post(self,request):
        serializer=CreateSaleSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        data=serializer.validated_data

       #create customer
        customer=None

        customer_name=data.get("customer_name")

        if customer_name:

            customer,created=Customer.objects.get_or_create(organization=request.user.organization,name=customer_name)

        #create sale
        sale=Sale.objects.create(
            organization=request.user.organization,
            customer=customer,
            invoice_number=generate_invoice_number(),
            payment_method=data["payment_method"],
            discount=data.get("discount",0),
            created_by=request.user
            )

        sub_total=Decimal("0.00")

            #create Sale Items

        for item in data["items"]:
            product=item["product"]
            quantity=item["quantity"]
            discount=Decimal(item.get("discount",0)) 

        #check stock
        if product.stock_quantity<quantity:

            return Response(
                {
                    "error":
                    f"Insufficent stock for {product.name}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )       

        item_subtotal=(
            product.selling_price*quantity)-discount

        SaleItem.objects.create(
             sale=sale,
             product=product,
             barcode=product.barcode,
             product_code=product.product_code,
             product_name=product.name,
             batch_number=product.batch_number,
             expiry_date=product.expiry_date,
             quantity=quantity,
             unit_price=product.selling_price,
             discount=discount,
             tax=0,
             subtotal=item_subtotal
        )

        subtotal +=item_subtotal

        #Reduce Inventory
        product.stock_quantity-=quantity

        product.save()

        #Calculate Bill Total

        sale.subtotal=subtotal

        sale.total=(
            sale.subtotal-sale.discount+sale.tax
        )
        sale.save()


        return Response(
            SaleSerializer(sale).data,
            status=status.HTTP_201_CREATED
        )


class SaleListAPIView(APIView):

    def get(self,request):
        sales=Sale.objects.filter(organization=request.user.organization)
        serializer=SaleSerializer(sales,many=True)

        return Response(serializer.data)

class SaleDetailAPIView(APIView):

    def get(self,request,id):

        sale=get_object_or_404(sale,id=id,organization=request.user.organization)    

        serializer=SaleSerializer(sale)

        return Response(serializer.data)

class ProductBarcodeAPIView(APIView):
    permission_classes=[
        IsAuthenticated
    ]   

    def get(self,request,barcode):
        product=get_object_or_404(Product,barcode=barcode,organization=request.user.organization)
        serializer=ProductBarcodeSerializer(product)

        return Response(serializer.data) 