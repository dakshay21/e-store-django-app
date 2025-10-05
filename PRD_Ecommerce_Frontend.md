# Product Requirements Document (PRD)
## E-commerce Frontend Application

### Overview
This PRD outlines the requirements for building a modern e-commerce frontend application using Next.js that integrates with the existing Django REST Framework backend API.

### Backend API Information
- **Base URL**: `http://localhost:8000/api/`
- **API Documentation**: Available at `http://localhost:8000/swagger/` (Swagger UI)
- **CORS**: Configured for `http://localhost:3000` and `http://127.0.0.1:3000`

---

## 1. Product Management APIs

### 1.1 Get All Products
- **Endpoint**: `GET /api/products/`
- **Description**: Retrieve paginated list of all products
- **Query Parameters**:
  - `page` (optional): Page number (default: 1)
  - `page_size` (optional): Items per page (default: 20, max: 100)
- **Response**: Paginated list with simplified product data
- **Use Case**: Product catalog/listing page

### 1.2 Get Product Details
- **Endpoint**: `GET /api/products/{id}/`
- **Description**: Retrieve detailed information about a specific product
- **Response**: Complete product information including stock status
- **Use Case**: Product detail page

### 1.3 Search Products
- **Endpoint**: `GET /api/products/search/?q={search_term}`
- **Description**: Search products by name or description
- **Query Parameters**:
  - `q` (required): Search term
- **Response**: List of matching products
- **Use Case**: Search functionality

### 1.4 Get In-Stock Products
- **Endpoint**: `GET /api/products/in-stock/`
- **Description**: Get only products that are currently in stock
- **Response**: List of available products
- **Use Case**: Filter products by availability

### 1.5 Create Product (Admin)
- **Endpoint**: `POST /api/products/`
- **Description**: Create a new product (admin functionality)
- **Request Body**: Complete product data
- **Use Case**: Admin product management

### 1.6 Update Product (Admin)
- **Endpoint**: `PUT /api/products/{id}/`
- **Description**: Update existing product (admin functionality)
- **Request Body**: Updated product data
- **Use Case**: Admin product management

### 1.7 Delete Product (Admin)
- **Endpoint**: `DELETE /api/products/{id}/`
- **Description**: Delete a product (admin functionality)
- **Use Case**: Admin product management

---

## 2. Order Management APIs

### 2.1 Get All Orders
- **Endpoint**: `GET /api/orders/`
- **Description**: Retrieve paginated list of all orders
- **Query Parameters**:
  - `page` (optional): Page number (default: 1)
  - `page_size` (optional): Items per page (default: 20, max: 100)
- **Response**: Paginated list with simplified order data
- **Use Case**: Order management dashboard

### 2.2 Get Order Details
- **Endpoint**: `GET /api/orders/{id}/`
- **Description**: Retrieve detailed information about a specific order
- **Response**: Complete order information including items
- **Use Case**: Order details page

### 2.3 Create Order
- **Endpoint**: `POST /api/orders/`
- **Description**: Create a new order
- **Request Body**: Order data with customer info and items
- **Response**: Created order with calculated total
- **Use Case**: Checkout process

### 2.4 Get Orders by Email
- **Endpoint**: `GET /api/orders/by-email/?email={customer_email}`
- **Description**: Retrieve orders for a specific customer
- **Query Parameters**:
  - `email` (required): Customer email address
- **Response**: List of customer orders
- **Use Case**: Customer order history

---

## 3. Cart Management APIs

### 3.1 Add to Cart
- **Endpoint**: `POST /api/cart/add/`
- **Description**: Add item to cart (simulation)
- **Request Body**:
  ```json
  {
    "product_id": 1,
    "quantity": 2
  }
  ```
- **Response**: Cart item confirmation
- **Use Case**: Add products to shopping cart

---

## 4. Data Models

### 4.1 Product Model
```typescript
interface Product {
  id: number;
  name: string;
  description: string;
  price: string; // Decimal as string
  image_url?: string;
  stock: number;
  is_in_stock: boolean;
  created_at: string; // ISO datetime
  updated_at: string; // ISO datetime
}
```

### 4.2 Product List Model (Simplified)
```typescript
interface ProductListItem {
  id: number;
  name: string;
  price: string;
  image_url?: string;
  stock: number;
  is_in_stock: boolean;
}
```

### 4.3 Order Model
```typescript
interface Order {
  id: number;
  customer_name: string;
  email: string;
  address: string;
  total_price: string; // Decimal as string
  items: OrderItem[];
  created_at: string; // ISO datetime
  updated_at: string; // ISO datetime
}
```

### 4.4 Order Item Model
```typescript
interface OrderItem {
  product_id: number;
  quantity: number;
}
```

### 4.5 Order List Model (Simplified)
```typescript
interface OrderListItem {
  id: number;
  customer_name: string;
  email: string;
  total_price: string;
  items_count: number;
  created_at: string;
}
```

### 4.6 Cart Item Model
```typescript
interface CartItem {
  product_id: number;
  product_name: string;
  price: string;
  quantity: number;
  total: string;
}
```

---

## 5. Frontend Application Requirements

### 5.1 Core Features
1. **Product Catalog**
   - Display all products with pagination
   - Product search functionality
   - Filter by availability (in-stock)
   - Product detail pages

2. **Shopping Cart**
   - Add/remove items from cart
   - Update quantities
   - Cart persistence (localStorage/sessionStorage)
   - Cart summary

3. **Order Management**
   - Create new orders
   - View order history by email
   - Order details page
   - Order confirmation

4. **Admin Panel** (Optional)
   - Product CRUD operations
   - Order management
   - Stock management

### 5.2 Technical Requirements
- **Framework**: Next.js 14+ with App Router
- **Styling**: TailwindCSS
- **State Management**: TanStack React Query for server state
- **UI Components**: Shadcn/ui
- **TypeScript**: Full TypeScript implementation

### 5.3 API Integration
- Use TanStack React Query for data fetching and caching
- Implement proper error handling
- Loading states for all async operations
- Optimistic updates where appropriate

### 5.4 Key Pages/Components
1. **Home Page**: Featured products, search bar
2. **Products Page**: Product grid with filters and pagination
3. **Product Detail Page**: Full product information, add to cart
4. **Cart Page**: Cart items, quantity updates, checkout
5. **Checkout Page**: Order form, order summary
6. **Order Confirmation**: Order details and confirmation
7. **Order History**: Customer order lookup by email
8. **Search Results**: Filtered product results

### 5.5 Error Handling
- Network error handling
- Validation error display
- Stock availability errors
- 404 handling for products/orders

### 5.6 Performance Considerations
- Image optimization for product images
- Lazy loading for product lists
- Pagination for large datasets
- Caching strategies with React Query

---

## 6. Sample API Responses

### 6.1 Products List Response
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "MacBook Pro 16\"",
      "price": "2499.99",
      "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500",
      "stock": 10,
      "is_in_stock": true
    }
  ]
}
```

### 6.2 Product Detail Response
```json
{
  "id": 1,
  "name": "MacBook Pro 16\"",
  "description": "Apple MacBook Pro with M2 Pro chip, 16GB RAM, 512GB SSD",
  "price": "2499.99",
  "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500",
  "stock": 10,
  "is_in_stock": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### 6.3 Order Creation Request
```json
{
  "customer_name": "John Doe",
  "email": "john.doe@example.com",
  "address": "123 Main St, City, State 12345",
  "items": [
    {
      "product_id": 1,
      "quantity": 1
    },
    {
      "product_id": 2,
      "quantity": 2
    }
  ]
}
```

---

## 7. Development Guidelines

### 7.1 Code Structure
- Use functional components with hooks
- Implement custom hooks for API calls
- Separate concerns (components, hooks, types, utils)
- Follow Next.js 14 App Router conventions

### 7.2 Styling Guidelines
- Use TailwindCSS utility classes
- Create reusable component variants
- Follow accessibility best practices

### 7.3 State Management
- Use React Query for server state
- Use React Context for client state
- Implement proper loading and error states
- Cache API responses appropriately

### 7.4 Testing
- Unit tests for utility functions
- Component tests for UI components
- Integration tests for API calls
- E2E tests for critical user flows

---

## 8. Deployment Considerations

### 8.1 Environment Variables
- API base URL configuration
- Environment-specific settings
- Feature flags for admin functionality

### 8.2 Build Optimization
- Next.js production build optimization
- Image optimization
- Bundle size optimization
- SEO optimization

---

This PRD provides a comprehensive guide for building a modern e-commerce frontend that integrates seamlessly with the existing Django REST Framework backend. The API endpoints are well-documented and ready for implementation in a Next.js application.
