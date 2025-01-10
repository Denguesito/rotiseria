# admin.py en la app 'pedidos'
from django.contrib import admin
from .models import Pedido

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_nombre', 'cliente_telefono', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('cliente_nombre', 'cliente_telefono')

    # Puedes agregar filtros adicionales para estadísticas
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset

admin.site.register(Pedido, PedidoAdmin)

