from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Order CRUD operations
    path('', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    
    # Additional order endpoints
    path('by-email/', views.order_by_email, name='order-by-email'),
    
    # Cart functionality
    path('cart/add/', views.add_to_cart, name='add-to-cart'),
]
