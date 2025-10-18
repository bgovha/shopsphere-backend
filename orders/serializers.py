from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'status', 'total_amount', 'items']
        read_only_fields = ['user']

class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['items']
        
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("At least one item is required")
        return value
        
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        total_amount = 0
        
        # Calculate total amount and validate stock
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for {product.name}. Available: {product.stock}"
                )
            
            total_amount += product.price * quantity
        
        # Create order
        order = Order.objects.create(
            user=self.context['request'].user,
            total_amount=total_amount
        )
        
        # Create order items and update stock
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )
            
            # Update product stock
            product.stock -= quantity
            product.save()
        
        return order

