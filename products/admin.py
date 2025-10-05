from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for Product model
    """
    list_display = [
        'id', 'name', 'price', 'stock', 'is_in_stock', 
        'created_at', 'updated_at'
    ]
    list_filter = ['created_at', 'updated_at', 'stock']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'image_url')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_in_stock(self, obj):
        """Display stock status"""
        return obj.is_in_stock
    is_in_stock.boolean = True
    is_in_stock.short_description = 'In Stock'
