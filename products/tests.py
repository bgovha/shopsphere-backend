from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Product


class ProductAPITest(TestCase):
    """Test Product API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create admin user
        self.admin = User.objects.create_user(
            username='admin',
            password='adminpass123',
            is_staff=True
        )
        
        # Create test category
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic items'
        )
        
        # Create test product
        self.product = Product.objects.create(
            name='Test Laptop',
            description='A test laptop',
            price=999.99,
            category=self.category,
            in_stock_quantity=10
        )
        
        # API client
        self.client = APIClient()
    
    def test_get_products_list(self):
        """Test retrieving product list"""
        response = self.client.get('/api/products/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Test Laptop')
    
    def test_get_single_product(self):
        """Test retrieving single product"""
        response = self.client.get(f'/api/products/{self.product.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Laptop')
        self.assertEqual(float(response.data['price']), 999.99)
    
    def test_search_products(self):
        """Test product search"""
        response = self.client.get('/api/products/?search=laptop')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_create_product_as_admin(self):
        """Test creating product as admin"""
        self.client.force_authenticate(user=self.admin)
        
        data = {
            'name': 'New Product',
            'description': 'A new product',
            'price': 49.99,
            'category_id': self.category.id,
            'in_stock_quantity': 20
        }
        
        response = self.client.post('/api/products/', data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
    
    def test_create_product_as_regular_user(self):
        """Test that regular users cannot create products"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            'name': 'Unauthorized Product',
            'description': 'Should not be created',
            'price': 99.99,
            'category_id': self.category.id,
            'in_stock_quantity': 5
        }
        
        response = self.client.post('/api/products/', data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)