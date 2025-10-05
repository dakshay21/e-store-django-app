from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model
    """
    is_in_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 
            'image_url', 'stock', 'is_in_stock', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_price(self, value):
        """Validate price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_stock(self, value):
        """Validate stock is non-negative"""
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value


class ProductListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for product listing
    """
    is_in_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image_url', 'stock', 'is_in_stock']
