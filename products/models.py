from django.db import models
from decimal import Decimal


class Product(models.Model):
    """
    Product model for e-commerce platform
    """
    name = models.CharField(max_length=200, help_text="Product name")
    description = models.TextField(help_text="Product description")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Product price"
    )
    image_url = models.URLField(
        max_length=500, 
        blank=True, 
        null=True,
        help_text="Product image URL"
    )
    stock = models.PositiveIntegerField(
        default=0,
        help_text="Available stock quantity"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        """Check if product is in stock"""
        return self.stock > 0

    def reduce_stock(self, quantity):
        """Reduce stock by given quantity"""
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
            return True
        return False
