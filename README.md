# E-commerce Backend API

A Django REST Framework backend for an e-commerce MVP with PostgreSQL database, featuring product management, order processing, and admin interface.

## Features

- **Product Management**: Full CRUD operations for products with inventory tracking
- **Order Processing**: Order creation with automatic stock reduction
- **Admin Interface**: Django admin for easy management
- **API Documentation**: Swagger/ReDoc documentation
- **PostgreSQL**: Production-ready database
- **CORS Support**: Ready for frontend integration

## Project Structure

```
ecommerce_backend/
├── ecommerce_backend/          # Main project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── products/                   # Products app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── orders/                     # Orders app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── manage.py
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites

- Docker and Docker Compose
- Git

### Quick Start with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ecommerce_backend
   ```

2. **Start the application**
   ```bash
   # Make the start script executable (if not already)
   chmod +x start.sh
   
   # Start development environment
   ./start.sh dev
   ```

3. **Access the application**
   - API: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin
   - API Documentation: http://localhost:8000/swagger/

### Manual Setup (Alternative)

#### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip

#### Setup Steps

1. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

4. **Setup PostgreSQL database**
   ```sql
   CREATE DATABASE ecommerce_db;
   CREATE USER postgres WITH PASSWORD 'postgres';
   GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO postgres;
   ```

5. **Run migrations**
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

6. **Populate sample data**
   ```bash
   python3 manage.py populate_data
   ```

7. **Create superuser**
   ```bash
   python3 manage.py createsuperuser
   ```

8. **Run development server**
   ```bash
   python3 manage.py runserver
   ```

## API Endpoints

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | List all products (paginated) |
| POST | `/api/products/` | Create new product |
| GET | `/api/products/{id}/` | Get product details |
| PUT | `/api/products/{id}/` | Update product |
| DELETE | `/api/products/{id}/` | Delete product |
| GET | `/api/products/search/?q=term` | Search products |
| GET | `/api/products/in-stock/` | Get products in stock |

### Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/orders/` | List all orders (paginated) |
| POST | `/api/orders/` | Create new order |
| GET | `/api/orders/{id}/` | Get order details |
| GET | `/api/orders/by-email/?email=user@example.com` | Get orders by email |

### Cart

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/cart/add/` | Add item to cart |

## API Documentation

- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`
- **Admin Panel**: `http://localhost:8000/admin/`

## Data Models

### Product Model

```python
{
    "id": 1,
    "name": "Product Name",
    "description": "Product description",
    "price": "99.99",
    "image_url": "https://example.com/image.jpg",
    "stock": 10,
    "is_in_stock": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

### Order Model

```python
{
    "id": 1,
    "customer_name": "John Doe",
    "email": "john@example.com",
    "address": "123 Main St, City, State",
    "total_price": "199.98",
    "items": [
        {
            "product_id": 1,
            "quantity": 2
        }
    ],
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

## Example API Usage

### Create a Product

```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": "999.99",
    "image_url": "https://example.com/laptop.jpg",
    "stock": 5
  }'
```

### Create an Order

```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "email": "john@example.com",
    "address": "123 Main St, City, State",
    "items": [
      {
        "product_id": 1,
        "quantity": 2
      }
    ]
  }'
```

### Add to Cart

```bash
curl -X POST http://localhost:8000/api/cart/add/ \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 1
  }'
```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### Database Configuration

The project is configured to use PostgreSQL by default. To use SQLite for development, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## Docker Commands

### Using the Start Script

```bash
# Start development environment
./start.sh dev

# Start production environment
./start.sh prod

# Build Docker images
./start.sh build

# Stop all containers
./start.sh stop

# Clean up containers and volumes
./start.sh clean

# View container logs
./start.sh logs

# Open shell in web container
./start.sh shell

# Show help
./start.sh help
```

### Manual Docker Commands

```bash
# Development
docker-compose up --build

# Production
docker-compose -f docker-compose.prod.yml up --build -d

# Stop containers
docker-compose down

# View logs
docker-compose logs -f

# Execute commands in container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## Development

### Running Tests

```bash
# With Docker
docker-compose exec web python manage.py test

# Without Docker
python3 manage.py test
```

### Creating Migrations

```bash
# With Docker
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Without Docker
python3 manage.py makemigrations
python3 manage.py migrate
```

### Loading Sample Data

```bash
# With Docker
docker-compose exec web python manage.py populate_data

# Without Docker
python3 manage.py populate_data
```

## Production Deployment

1. Set `DEBUG=False` in production
2. Use environment variables for sensitive data
3. Configure proper database credentials
4. Set up static file serving
5. Use a production WSGI server (e.g., Gunicorn)
6. Configure reverse proxy (e.g., Nginx)

## Future Enhancements

- User authentication and authorization
- Payment gateway integration
- Email notifications
- Order status tracking
- Product categories and tags
- Inventory management
- Analytics and reporting
- Caching layer
- API rate limiting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
