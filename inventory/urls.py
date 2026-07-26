from django.urls import path
from .views import (SupplierListCreateAPIView,SupplierDetailAPIView, ProductListCreateAPIView,ProductDetailAPIView)
from .views import (StockInListCreateAPIView,StockInDetailAPIView)
from .views import (StockOutListCreateAPIView,StockOutDetailAPIView)
from .views import ViewStockAPIView

urlpatterns=[


    path("suppliers/",SupplierListCreateAPIView.as_view(),name="supplier-list"),
    path("suppliers/<int:id>/",SupplierDetailAPIView.as_view(),name="supplier-detail"),
    path("products/",ProductListCreateAPIView.as_view()),
    path("products/<int:id>/",ProductDetailAPIView.as_view()),
    path("stock-in/",StockInListCreateAPIView.as_view(),name="stock-in-list"),
    path("stock-in/<int:id>/",StockInDetailAPIView.as_view(),name="stock-in-detail"),
    path("stock-out/",StockOutListCreateAPIView.as_view(),name="stock-out-list"),
    path("stock-out/<int:id>/",StockOutDetailAPIView.as_view(),name="stock-out-detail"),
    path("stock/",ViewStockAPIView.as_view(),name="view-stock"),
]