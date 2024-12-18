from django.views.generic import ListView, DetailView
from .models import Productos

# Vista para listar todos los productos
class ProductoListView(ListView):
    model = Productos
    template_name = 'productos/lista_productos.html'  # Plantilla para la lista
    context_object_name = 'productos'  # Nombre del contexto en la plantilla

# Vista para mostrar los detalles de un producto
class ProductoDetailView(DetailView):
    model = Productos
    template_name = 'productos/detalle_producto.html'  # Plantilla para los detalles
    context_object_name = 'producto'

