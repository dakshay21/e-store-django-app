from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Order
from .serializers import OrderSerializer, OrderListSerializer
from products.models import Product


class OrderPagination(PageNumberPagination):
    """Custom pagination for orders"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class OrderListCreateView(generics.ListCreateAPIView):
    """
    List all orders or create a new order
    GET /orders/ - List orders with pagination
    POST /orders/ - Create new order
    """
    queryset = Order.objects.all()
    pagination_class = OrderPagination
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderListSerializer
        return OrderSerializer


class OrderDetailView(generics.RetrieveAPIView):
    """
    Retrieve order details
    GET /orders/{id}/ - Get order details
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


@api_view(['POST'])
def add_to_cart(request):
    """
    Add item to cart (simulate cart functionality)
    POST /cart/add/
    """
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)
    
    if not product_id:
        return Response(
            {'error': 'Product ID is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {'error': 'Product not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    if not product.is_in_stock:
        return Response(
            {'error': 'Product is out of stock'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if product.stock < quantity:
        return Response(
            {'error': f'Only {product.stock} items available in stock'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # In a real application, this would be stored in session or user's cart
    # For MVP, we'll just return the cart item data
    cart_item = {
        'product_id': product.id,
        'product_name': product.name,
        'price': str(product.price),
        'quantity': quantity,
        'total': str(product.price * quantity)
    }
    
    return Response({
        'message': 'Item added to cart',
        'cart_item': cart_item
    })


@api_view(['GET'])
def order_by_email(request):
    """
    Get orders by customer email
    GET /orders/by-email/?email=customer@example.com
    """
    email = request.GET.get('email', '').strip()
    
    if not email:
        return Response(
            {'error': 'Email parameter is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    orders = Order.objects.filter(email__iexact=email)
    serializer = OrderListSerializer(orders, many=True)
    return Response(serializer.data)
