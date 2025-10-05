from django.db import models
from decimal import Decimal
import json


class Order(models.Model):
    """
    Order model for e-commerce platform
    """
    customer_name = models.CharField(max_length=100, help_text="Customer name")
    email = models.EmailField(help_text="Customer email")
    address = models.TextField(help_text="Delivery address")
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Total order price"
    )
    items = models.JSONField(
        help_text="Order items as JSON (product IDs and quantities)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

    @property
    def items_list(self):
        """Return items as a list for easier handling"""
        return self.items if isinstance(self.items, list) else []

    def add_item(self, product_id, quantity):
        """Add an item to the order"""
        items = self.items_list.copy()
        
        # Check if product already exists in order
        for item in items:
            if item.get('product_id') == product_id:
                item['quantity'] += quantity
                break
        else:
            # Add new item
            items.append({
                'product_id': product_id,
                'quantity': quantity
            })
        
        self.items = items
        self.save()

    def calculate_total(self, products_data):
        """Calculate total price based on products data"""
        total = Decimal('0.00')
        for item in self.items_list:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 0)
            
            # Find product price in products_data
            for product in products_data:
                if product['id'] == product_id:
                    total += Decimal(str(product['price'])) * quantity
                    break
        
        return total
