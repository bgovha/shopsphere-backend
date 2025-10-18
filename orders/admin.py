from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Display order items inline with order"""
    model = OrderItem
    extra = 0  # Don't show empty forms
    readonly_fields = ('product', 'quantity', 'price_at_purchase')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for orders"""
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('total_amount', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'status', 'total_amount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def has_add_permission(self, request):
        """Disable manual order creation (should be done via API)"""
        return False


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin interface for order items"""
    list_display = ('id', 'order', 'product', 'quantity', 'price_at_purchase')
    list_filter = ('order__status',)
    search_fields = ('product__name', 'order__user__username')
    readonly_fields = ('order', 'product', 'quantity', 'price_at_purchase')
    
    def has_add_permission(self, request):
        """Disable manual creation"""
        return False