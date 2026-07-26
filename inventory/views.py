from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Supplier,Product,StockIn,StockOut
from .serializers import SupplierSerializer,ProductSerializer,StockInSerializer,StockOutSerializer
from django.core.exceptions import ValidationError

from .serializers import StockSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework import status



# Create your views here.
class SupplierListCreateAPIView(APIView):
    permission_classes=[
        IsAuthenticated
    ]

    def get(self,request):
        suppliers=Supplier.objects.filter(organization=request.user.organization)

        serializer=SupplierSerializer(suppliers,many=True)

        return Response(serializer.data)
    
    def post(self,request):

        serializer=SupplierSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(organization=request.user.organization)

            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class SupplierDetailAPIView(APIView):
    permission_classes=[
        IsAuthenticated
    ]

    def get_object(self,request,id):
        return get_object_or_404(Supplier,id=id,organization=request.user.organization)
    
    def get(self,request,id):
        supplier=self.get_object(request,id)

        serializer=SupplierSerializer(supplier)

        return Response(serializer.data)
    
    def put(self,request,id):
        supplier=self.get_object(request,id)

        serializer=SupplierSerializer(supplier,data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors,status=400)
    
    def delete(self,request,id):
        supplier=self.get_object(request,id)

        supplier.delete()
        return Response({"message":"Supplier deleted"})
    

class ProductListCreateAPIView(APIView):
    permission_classes=[
       IsAuthenticated
    ]

    def get(self,request):
        products=Product.objects.filter(organization=request.user.organization)
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data)
    

    def post(self,request):
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
            organization=request.user.organization)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=400)
    
class ProductDetailAPIView(APIView):
    permission_classes=[
        IsAuthenticated
    ]    

    def get_object(self,request,id):   
      return get_object_or_404(Product,id=id,organization=request.user.organization)
    

    def get(self,request,id):
        product=self.get_object(request,id)
        serializer=ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self,request,id):
        product=self.get_object(request,id)
        serializer=ProductSerializer(product,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors,status=400)
    
    def delete(self,request,id):
        product=self.get_object(request,id)
        product.delete()

        return Response({"message":"Product deleted"})
    

class StockInListCreateAPIView(APIView):
    permission_classes = [
        IsAuthenticated
    ]    

    def get(self, request):

        stockins = StockIn.objects.filter(
            organization=request.user.organization
        )

        serializer = StockInSerializer(
            stockins,
            many=True
        )

        return Response(serializer.data)



    def post(self, request):

        serializer = StockInSerializer(
            data=request.data
        )


        if serializer.is_valid():

            # DO NOT UPDATE PRODUCT STOCK HERE
            # StockIn model save() handles it

            stockin = serializer.save(
                organization=request.user.organization,
                created_by=request.user
            )


            return Response(
                StockInSerializer(stockin).data,
                status=status.HTTP_201_CREATED
            )


        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



class StockInDetailAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get_object(self,request,id):

        return get_object_or_404(
            StockIn,
            id=id,
            organization=request.user.organization
        )



    def get(self,request,id):

        stockin = self.get_object(
            request,
            id
        )

        serializer = StockInSerializer(stockin)

        return Response(serializer.data)



    def put(self,request,id):

        stockin = self.get_object(
            request,
            id
        )


        old_quantity = stockin.quantity


        serializer = StockInSerializer(
            stockin,
            data=request.data
        )


        if serializer.is_valid():

            new_quantity = serializer.validated_data["quantity"]

            product = stockin.product


            # adjust stock difference only

            difference = new_quantity - old_quantity


            product.stock += difference

            product.save()


            serializer.save()


            return Response(
                serializer.data
            )


        return Response(
            serializer.errors,
            status=400
        )



    def delete(self,request,id):

        stockin = self.get_object(
            request,
            id
        )


        # StockIn model delete()
        # automatically reduces stock

        stockin.delete()


        return Response(
            {
                "message":"Stock In deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )





class StockOutListCreateAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self,request):

        queryset = StockOut.objects.filter(
            organization=request.user.organization
        ).order_by("-date")


        serializer = StockOutSerializer(
            queryset,
            many=True
        )

        return Response(serializer.data)



    def post(self,request):

        serializer = StockOutSerializer(
            data=request.data
        )


        if serializer.is_valid():

            product = serializer.validated_data["product"]

            quantity = serializer.validated_data["quantity"]


            if product.stock < quantity:

                return Response(
                    {
                        "error":"Not enough stock available"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )


            # DO NOT REDUCE STOCK HERE
            # StockOut model save() handles it


            stock_out = serializer.save(
                organization=request.user.organization,
                created_by=request.user
            )


            return Response(
                StockOutSerializer(stock_out).data,
                status=status.HTTP_201_CREATED
            )


        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )





class StockOutDetailAPIView(APIView):

    permission_classes=[
        IsAuthenticated
    ]


    def get_object(self,request,id):

        return get_object_or_404(
            StockOut,
            id=id,
            organization=request.user.organization
        )



    def get(self,request,id):

        stock_out = self.get_object(
            request,
            id
        )


        serializer = StockOutSerializer(stock_out)


        return Response(serializer.data)




    def put(self,request,id):

        stock_out = self.get_object(
            request,
            id
        )


        old_quantity = stock_out.quantity


        serializer = StockOutSerializer(
            stock_out,
            data=request.data
        )


        if serializer.is_valid():

            new_quantity = serializer.validated_data["quantity"]


            product = stock_out.product



            # restore old stock first

            product.stock += old_quantity



            # check new quantity

            if product.stock < new_quantity:

                return Response(
                    {
                        "error":"Not enough stock available"
                    },
                    status=400
                )



            # subtract new quantity

            product.stock -= new_quantity


            product.save()



            serializer.save()



            return Response(
                serializer.data
            )


        return Response(
            serializer.errors,
            status=400
        )




    def delete(self,request,id):

        stock_out = self.get_object(
            request,
            id
        )


        # StockOut model delete()
        # automatically restores stock

        stock_out.delete()


        return Response(
            {
                "message":"Stock Out deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )





class ViewStockAPIView(APIView):

    permission_classes=[
        IsAuthenticated
    ]


    def get(self,request):

        products = Product.objects.filter(
            organization=request.user.organization
        )


        serializer = StockSerializer(
            products,
            many=True
        )


        return Response(serializer.data)