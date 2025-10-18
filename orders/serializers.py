from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductListSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for individual items in an order"""
    product = ProductListSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price_at_purchase', 'total_price']
        read_only_fields = ['id', 'price_at_purchase']
    
    def get_total_price(self, obj):
        return obj.get_total_price()


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for viewing orders"""
    items = OrderItemSerializer(many=True, read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user_username', 'total_amount', 'status', 'created_at', 'updated_at', 'items']
        read_only_fields = ['id', 'total_amount', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new orders"""
    items = serializers.ListField(
        child=serializers.DictField(),
        write_only=True
    )
    
    class Meta:
        model = Order
        fields = ['items']
    
    def validate_items(self, value):
        """Validate that items list is not empty and has required fields"""
        if not value:
            raise serializers.ValidationError("Order must contain at least one item.")
        
        for item in value:
            if 'product_id' not in item or 'quantity' not in item:
                raise serializers.ValidationError("Each item must have 'product_id' and 'quantity'.")
            
            if item['quantity'] <= 0:
                raise serializers.ValidationError("Quantity must be greater than zero.")
        
        return value
    
    def create(self, validated_data):
        """Create order with items"""
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        # Calculate total
        from products.models import Product
        total_amount = 0
        order_items = []
        
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            quantity = item_data['quantity']
            
            # Check stock
            if product.in_stock_quantity < quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for {product.name}. Available: {product.in_stock_quantity}"
                )
            
            # Calculate price
            item_total = product.price * quantity
            total_amount += item_total
            
            # Store for later creation
            order_items.append({
                'product': product,
                'quantity': quantity,
                'price': product.price
            })
        
        # Create order
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            status='pending'
        )
        
        # Create order items and update stock
        for item in order_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price_at_purchase=item['price']
            )
            
            # Reduce stock
            item['product'].in_stock_quantity -= item['quantity']
            item['product'].save()
        
        return order
    
    