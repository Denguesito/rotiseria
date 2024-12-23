from django import forms
from .models import Carrito, CarritoItem
from apps.productos.models import Productos 


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


class AgregarProductoForm(forms.ModelForm):
    """Formulario para agregar productos al carrito."""
    class Meta:
        model = CarritoItem
        fields = ['producto', 'cantidad']
        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
        }
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

class AgregarCantidadProductoForm(forms.Form):
    """Formulario para elegir la cantidad de un producto antes de agregarlo al carrito."""
    cantidad = forms.IntegerField(min_value=1, initial=1, label="Cantidad", widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}))

    def __init__(self, *args, **kwargs):
        producto = kwargs.pop('producto', None)
        super().__init__(*args, **kwargs)
        if producto:
            self.fields['producto'] = forms.ModelChoiceField(queryset=Productos.objects.filter(id=producto.id), initial=producto, widget=forms.HiddenInput())
