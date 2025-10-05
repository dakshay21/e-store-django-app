from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for Order model
    """
    list_display = [
        'id', 'customer_name', 'email', 'total_price', 
        'items_count', 'created_at'
    ]
    list_filter = ['created_at', 'updated_at']
    search_fields = ['customer_name', 'email']
    readonly_fields = ['created_at', 'updated_at', 'total_price']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'email', 'address')
        }),
        ('Order Details', {
            'fields': ('total_price', 'items')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def items_count(self, obj):
        """Display number of items in order"""
        return sum(item.get('quantity', 0) for item in obj.items_list)
    items_count.short_description = 'Items Count'
    
    def get_readonly_fields(self, request, obj=None):
        """Make total_price readonly for existing orders"""
        if obj:  # editing an existing object
            return self.readonly_fields + ['items']
        return self.readonly_fields
