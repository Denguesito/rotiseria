from django.contrib import admin
from .models import Pedido, EstadisticaVenta
from django.urls import path
from .views import EstadisticasVentasView

class CustomAdminSite(admin.AdminSite):
    site_header = "Panel de Administración"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('estadisticas/', self.admin_view(EstadisticasVentasView.as_view()), name='estadisticas_ventas'),
        ]
        return custom_urls + urls

    def each_context(self, request):
        context = super().each_context(request)
        context['estadisticas_url'] = 'admin/pedidos/estadisticas/' 
        return context

admin_site = CustomAdminSite(name='custom_admin')
admin.site = admin_site

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_nombre', 'cliente_telefono', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    search_fields = ('cliente_nombre', 'cliente_telefono')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset
admin_site.register(Pedido, PedidoAdmin)

class EstadisticaVentaAdmin(admin.ModelAdmin):
    list_display = ('fecha_inicio', 'fecha_fin', 'total_ventas')
    list_filter = ('fecha_inicio', 'fecha_fin')
    search_fields = ('fecha_inicio', 'fecha_fin')
admin_site.register(EstadisticaVenta, EstadisticaVentaAdmin)
