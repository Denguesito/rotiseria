from django.contrib import admin
from .models import Productos
from apps.pedidos.admin import admin_site  # Importar el admin_site personalizado

# Registro del modelo Producto en el admin personalizado
@admin.register(Productos)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'descripcion')  # Columnas visibles
    search_fields = ('nombre',)  # Barra de búsqueda
    list_filter = ('precio',)  # Puedes agregar más filtros si lo deseas

# Alternativamente, puedes registrar el modelo sin usar el decorador @admin.register:
admin_site.register(Productos, ProductoAdmin)
