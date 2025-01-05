from django.contrib import admin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import format_html
from .models import (
    Customer,
    Product,
    Cart,
    OrderPlaced
)

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']
    list_filter = ['state', 'city']
    search_fields = ['name', 'locality', 'city', 'state']
    
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'product_image']
    list_filter = ['category', 'brand']
    search_fields = ['title', 'brand', 'category']
    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']
    list_filter = ['user']
    search_fields = ['user__username', 'product__title']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'amount', 'invoice']
    list_filter = ['status', 'ordered_date']
    search_fields = ['user__username', 'customer__name', 'product__title']
    date_hierarchy = 'ordered_date'
    list_per_page = 20
    
    def amount(self, obj):
        return f'₹{obj.quantity * obj.product.discounted_price}'
    amount.short_description = 'Total Amount'
    
    def invoice(self, obj):
        return format_html(f'<a class="button" href="/order-invoice/{obj.id}/">View Invoice</a>')
    invoice.short_description = 'Invoice'
    
    actions = ['mark_as_delivered', 'mark_as_shipped', 'mark_as_pending']
    
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='Delivered')
    mark_as_delivered.short_description = "Mark selected orders as delivered"
    
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='Shipped')
    mark_as_shipped.short_description = "Mark selected orders as shipped"
    
    def mark_as_pending(self, request, queryset):
        queryset.update(status='Pending')
    mark_as_pending.short_description = "Mark selected orders as pending"