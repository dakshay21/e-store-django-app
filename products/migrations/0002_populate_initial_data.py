# Generated manually for data migration

from django.db import migrations
from decimal import Decimal


def populate_products(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    
    products_data = [
        {
            'name': 'MacBook Pro 16"',
            'description': 'Apple MacBook Pro with M2 Pro chip, 16GB RAM, 512GB SSD',
            'price': Decimal('2499.99'),
            'image_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500',
            'stock': 10
        },
        {
            'name': 'iPhone 15 Pro',
            'description': 'Latest iPhone with titanium design and A17 Pro chip',
            'price': Decimal('999.99'),
            'image_url': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=500',
            'stock': 25
        },
        {
            'name': 'Sony WH-1000XM5',
            'description': 'Industry-leading noise canceling wireless headphones',
            'price': Decimal('399.99'),
            'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500',
            'stock': 15
        },
        {
            'name': 'Dell XPS 13',
            'description': 'Ultra-thin laptop with 13.4" InfinityEdge display',
            'price': Decimal('1299.99'),
            'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500',
            'stock': 8
        },
        {
            'name': 'Samsung Galaxy S24',
            'description': 'Android flagship with advanced AI features',
            'price': Decimal('799.99'),
            'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500',
            'stock': 20
        },
        {
            'name': 'iPad Air',
            'description': 'Powerful tablet with M2 chip and 10.9" Liquid Retina display',
            'price': Decimal('599.99'),
            'image_url': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500',
            'stock': 12
        },
        {
            'name': 'AirPods Pro',
            'description': 'Active noise cancellation with spatial audio',
            'price': Decimal('249.99'),
            'image_url': 'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=500',
            'stock': 30
        },
        {
            'name': 'Nintendo Switch',
            'description': 'Hybrid gaming console for home and on-the-go',
            'price': Decimal('299.99'),
            'image_url': 'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=500',
            'stock': 18
        },
        {
            'name': 'Canon EOS R5',
            'description': 'Professional mirrorless camera with 45MP sensor',
            'price': Decimal('3899.99'),
            'image_url': 'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=500',
            'stock': 5
        },
        {
            'name': 'Apple Watch Series 9',
            'description': 'Smartwatch with health monitoring and fitness tracking',
            'price': Decimal('399.99'),
            'image_url': 'https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=500',
            'stock': 22
        }
    ]

    for product_data in products_data:
        Product.objects.get_or_create(
            name=product_data['name'],
            defaults=product_data
        )


def populate_orders(apps, schema_editor):
    Order = apps.get_model('orders', 'Order')
    Product = apps.get_model('products', 'Product')
    
    orders_data = [
        {
            'customer_name': 'John Smith',
            'email': 'john.smith@email.com',
            'address': '123 Main Street, New York, NY 10001',
            'items': [
                {'product_id': 1, 'quantity': 1},
                {'product_id': 7, 'quantity': 2}
            ]
        },
        {
            'customer_name': 'Sarah Johnson',
            'email': 'sarah.johnson@email.com',
            'address': '456 Oak Avenue, Los Angeles, CA 90210',
            'items': [
                {'product_id': 2, 'quantity': 1},
                {'product_id': 6, 'quantity': 1}
            ]
        },
        {
            'customer_name': 'Mike Wilson',
            'email': 'mike.wilson@email.com',
            'address': '789 Pine Road, Chicago, IL 60601',
            'items': [
                {'product_id': 3, 'quantity': 1},
                {'product_id': 8, 'quantity': 1}
            ]
        },
        {
            'customer_name': 'Emily Davis',
            'email': 'emily.davis@email.com',
            'address': '321 Elm Street, Houston, TX 77001',
            'items': [
                {'product_id': 4, 'quantity': 1},
                {'product_id': 10, 'quantity': 1}
            ]
        },
        {
            'customer_name': 'David Brown',
            'email': 'david.brown@email.com',
            'address': '654 Maple Drive, Phoenix, AZ 85001',
            'items': [
                {'product_id': 5, 'quantity': 2},
                {'product_id': 9, 'quantity': 1}
            ]
        }
    ]

    for order_data in orders_data:
        # Calculate total price
        total_price = Decimal('0.00')
        for item in order_data['items']:
            try:
                product = Product.objects.get(id=item['product_id'])
                total_price += product.price * item['quantity']
            except Product.DoesNotExist:
                continue

        Order.objects.create(
            customer_name=order_data['customer_name'],
            email=order_data['email'],
            address=order_data['address'],
            total_price=total_price,
            items=order_data['items']
        )


def reverse_populate_data(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    Order = apps.get_model('orders', 'Order')
    
    Product.objects.all().delete()
    Order.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_products, reverse_populate_data),
        migrations.RunPython(populate_orders, reverse_populate_data),
    ]
