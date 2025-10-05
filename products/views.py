from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer, ProductListSerializer


class ProductPagination(PageNumberPagination):
    """Custom pagination for products"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductListCreateView(generics.ListCreateAPIView):
    """
    List all products or create a new product
    GET /products/ - List products with pagination
    POST /products/ - Create new product (admin only)
    """
    queryset = Product.objects.all()
    pagination_class = ProductPagination
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductListSerializer
        return ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a product
    GET /products/{id}/ - Get product details
    PUT /products/{id}/ - Update product (admin only)
    DELETE /products/{id}/ - Delete product (admin only)
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@api_view(['GET'])
def product_search(request):
    """
    Search products by name or description
    GET /products/search/?q=search_term
    """
    query = request.GET.get('q', '').strip()
    
    if not query:
        return Response(
            {'error': 'Search query is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    products = Product.objects.filter(
        name__icontains=query
    ) | Product.objects.filter(
        description__icontains=query
    )
    
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def products_in_stock(request):
    """
    Get only products that are in stock
    GET /products/in-stock/
    """
    products = Product.objects.filter(stock__gt=0)
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)
