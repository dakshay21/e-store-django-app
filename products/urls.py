from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Product CRUD operations
    path('', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    
    # Additional product endpoints
    path('search/', views.product_search, name='product-search'),
    path('in-stock/', views.products_in_stock, name='products-in-stock'),
]
