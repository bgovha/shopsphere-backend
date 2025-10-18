from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet for Order operations"""
    queryset = Order.objects.all()  # Add this line
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Users can only see their own orders"""
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new order"""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        return Response({
            'order': OrderSerializer(order).data,
            'message': 'Order created successfully'
        }, status=status.HTTP_201_CREATED)