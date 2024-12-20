from django.views.generic import ListView, DetailView, TemplateView
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

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrupar productos por categoría
        categorias = Productos.CATEGORIAS
        productos_por_categoria = {
            categoria[0]: Productos.objects.filter(categoria=categoria[0])
            for categoria in categorias
        }
        context['productos_por_categoria'] = productos_por_categoria
        return context