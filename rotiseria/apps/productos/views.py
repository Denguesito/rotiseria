from django.views.generic import ListView, DetailView
from .models import Productos

class ListaProductosView(ListView):
    model = Productos
    template_name = 'productos/lista.html'
    context_object_name = 'productos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categorias = Productos.CATEGORIAS
        context['productos_por_categoria'] = {
            categoria[0]: Productos.objects.filter(categoria=categoria[0])
            for categoria in categorias
        }
        return context

class DetallesProductoView(DetailView):
    model = Productos
    template_name = 'productos/detalles.html'
    context_object_name = 'producto'
