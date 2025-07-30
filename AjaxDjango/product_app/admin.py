"""
Admin configuration for the product_app application.
"""
from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """Admin interface for Producto model."""
    list_display = ('codigo', 'nombre', 'precio', 'cantidad', 'fecha')
    search_fields = ('codigo', 'nombre')
    list_filter = ('fecha',)