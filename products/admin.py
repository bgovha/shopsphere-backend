from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for categories"""
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for products"""
    list_display = ('id', 'name', 'category', 'price', 'in_stock_quantity', 'date_created')
    list_filter = ('category', 'date_created', 'in_stock_quantity')
    search_fields = ('name', 'description')
    list_editable = ('price', 'in_stock_quantity')  # Edit directly in list view
    ordering = ('-date_created',)
    readonly_fields = ('date_created', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'in_stock_quantity')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Timestamps', {
            'fields': ('date_created', 'updated_at'),
            'classes': ('collapse',)  # Collapsible section
        }),
    )
    