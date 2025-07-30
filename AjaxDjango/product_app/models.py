"""
Models for the product_app application.
"""
from django.db import models

class Producto(models.Model):
    """
    Model representing a product in the database.
    This model will be used across different database engines.
    """
    codigo = models.CharField(max_length=50, verbose_name="Código")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    cantidad = models.IntegerField(verbose_name="Cantidad")
    fecha = models.DateField(verbose_name="Fecha")

    class Meta:
        db_table = 'PRODUCTO2'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"