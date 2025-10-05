from rest_framework import serializers
from .models import Order
from products.models import Product
from decimal import Decimal


class OrderItemSerializer(serializers.Serializer):
    """
    Serializer for order items
    """
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        """Validate product exists and is in stock"""
        try:
            product = Product.objects.get(id=value)
            if not product.is_in_stock:
                raise serializers.ValidationError("Product is out of stock.")
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model
    """
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'customer_name', 'email', 'address', 
            'total_price', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_price', 'created_at', 'updated_at']

    def validate_items(self, value):
        """Validate items list is not empty"""
        if not value:
            raise serializers.ValidationError("Order must contain at least one item.")
        return value

    def validate_email(self, value):
        """Validate email format"""
        if not value or '@' not in value:
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def create(self, validated_data):
        """Create order with calculated total price"""
        items_data = validated_data.pop('items')
        
        # Calculate total price
        total_price = Decimal('0.00')
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            total_price += product.price * item_data['quantity']
        
        # Create order
        order = Order.objects.create(
            total_price=total_price,
            items=items_data,
            **validated_data
        )
        
        # Reduce stock for each product
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            if not product.reduce_stock(item_data['quantity']):
                raise serializers.ValidationError(
                    f"Insufficient stock for product: {product.name}"
                )
        
        return order


class OrderListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for order listing
    """
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'customer_name', 'email', 'total_price', 
            'items_count', 'created_at'
        ]
    
    def get_items_count(self, obj):
        """Get total number of items in the order"""
        return sum(item.get('quantity', 0) for item in obj.items_list)
