from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Supplier,Product,StockIn,StockOut
from .serializers import SupplierSerializer,ProductSerializer,StockInSerailizer,StockOutSeralizer
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
        return get_object_or_404(Supplier,id,organization=request.user.organization)
    
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
    permission_classes=[
        IsAuthenticated
    ]    

    def get(self,request):
        stockins=StockIn.objects.filter(organization=request.user.organization)
        serializer=StockInSerailizer(stockins,many=True)

        return Response(serializer.data)
    
    def post(self,request):
        serializer=StockInSerailizer(data=request.data)
        if serializer.is_valid():
            serializer.save(organization=request.user.organization,created_by=request.user)
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)
    

class StockInDetailAPIView(APIView):
    permission_classes=[
        IsAuthenticated
    ]

    def get(self,request,id):
        stockin=get_object_or_404(StockIn,id=id,organization=request.user.organization)
        serializer=StockInSerailizer(stockin)
        return Response(serializer.data)
    def delete(self,request,id):
        stockin=get_object_or_404(StockIn,id=id, organization=request.user.organization)
        stockin.delete()

        return Response({"message":"Stock entry deleted"})
    

class StockOutListCreateAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        queryset=StockOut.objects.filter(organization=request.user.organization).order_by("-date")
        serializer=StockOutSeralizer(queryset,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=StockOutSeralizer(data=request.data)

        if serializer.is_valid():
            serializer.save(organization=request.user.organization,created_by=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=400)


class StockOutDetailAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def get_object(self,request,id):
        return get_object_or_404(StockOut,id=id,organization=request.user.organization)
    
    def get(self,request,id):
        stock_out=self.get_objeect(request.id)
        serializer=StockOutSeralizer(stock_out)
        return Response(serializer.data)
    
    def delete(self,request,id):
        stock_out=self.get_object(request,id)
        stock_out.delete()

        return Response({
            "message":"Stock out record deleted sucessfully"
        })
    
class ViewStockAPIView(APIView):

    permission_classes=[
        IsAuthenticated
    ]

    def get(self,request):
        product=Product.objects.filter(organization=request.user.organization)
        serializer=StockSerializer(product,many=True)
        return Response(serializer.data)
    
    
