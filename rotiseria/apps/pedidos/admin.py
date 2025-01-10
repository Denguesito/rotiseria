from django.contrib import admin
from .models import Pedido , EstadisticaVenta

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_nombre', 'cliente_telefono', 'fecha_creacion') 
    list_filter = ('fecha_creacion',) 
    search_fields = ('cliente_nombre', 'cliente_telefono')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset

admin.site.register(Pedido, PedidoAdmin)

class EstadisticaVentaAdmin(admin.ModelAdmin):
    list_display = ('fecha_inicio', 'fecha_fin', 'total_ventas')
    list_filter = ('fecha_inicio', 'fecha_fin')
    search_fields = ('fecha_inicio', 'fecha_fin')

admin.site.register(EstadisticaVenta, EstadisticaVentaAdmin)
