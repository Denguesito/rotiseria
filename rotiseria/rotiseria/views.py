from django.views.generic import TemplateView
from apps.productos.models import Productos

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrupamos productos por categoría
        categorias = Productos.CATEGORIAS
        productos_por_categoria = {
            categoria[0]: Productos.objects.filter(categoria=categoria[0])
            for categoria in categorias
        }
        context['productos_por_categoria'] = productos_por_categoria
        return context


