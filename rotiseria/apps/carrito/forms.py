from django import forms
from .models import Carrito


class CarritoForm(forms.ModelForm):
    """Formulario para los datos del cliente."""
    
    class Meta:
        model = Carrito
        fields = ['cliente_nombre', 'cliente_telefono']
        labels = {
            'cliente_nombre': 'Nombre completo',
            'cliente_telefono': 'Teléfono',
        }
        widgets = {
            'cliente_nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu nombre'}),
            'cliente_telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu teléfono'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer que los campos son obligatorios
        self.fields['cliente_nombre'].required = True
        self.fields['cliente_telefono'].required = True


class AgregarCantidadProductoForm(forms.Form):
    """Formulario para elegir la cantidad de un producto antes de agregarlo al carrito."""
    cantidad = forms.IntegerField(
        min_value=1,
        initial=1,
        label="Cantidad",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1})
    )

