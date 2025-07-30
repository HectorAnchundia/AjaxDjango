"""
Forms for the product_app application.
"""
from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    """Form for creating and updating Producto objects."""
    
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'precio', 'cantidad', 'fecha']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }