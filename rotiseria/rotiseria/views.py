from django.views.generic import TemplateView
from apps.productos.models import Productos

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Categorías de productos
        categorias = Productos.CATEGORIAS
        productos_por_categoria = {
            categoria[0]: Productos.objects.filter(categoria=categoria[0])
            for categoria in categorias
        }

        # Diccionario con las imágenes de las categorías
        imagenes_categorias = {
            'Pizzas': '/static/img/pizza.jpg',
            'Hamburguesas': '/static/img/hamburgesa.jpg',
            'Lomitos': '/static/img/lomitook.jpg',
            'Sandwich de milanesa': '/static/img/milanesa.jpg',
            'Papas fritas': '/static/img/frita.jpg',
        }
        

        # Agregar imágenes con valor predeterminado para categorías sin imagen
        categorias_con_imagenes = {
            categoria[0]: imagenes_categorias.get(categoria[0], '/static/img/default.jpg')
            for categoria in categorias
        }

        context['productos_por_categoria'] = productos_por_categoria
        context['imagenes_categorias'] = categorias_con_imagenes
        return context
