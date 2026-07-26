from django.urls import path
from .views import (CreateSaleAPIView,SaleListAPIView,SaleDetailAPIView,ProductBarcodeAPIView)

urlpatterns = [
    path("create/",CreateSaleAPIView.as_view(),name="create-sale"),
    path("",SaleListAPIView.as_view(),name="sale-list"),
    path("<int:id>/",SaleDetailAPIView.as_view(),name="sale-detail"),
    path("product/barcode/<str:barcode>/",ProductBarcodeAPIView.as_view(),name="barcode-product"),
    path("products/barcode/<str:barcode>/",ProductBarcodeAPIView.as_view(),name="product-barcode"),
]