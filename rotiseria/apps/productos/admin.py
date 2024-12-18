from django.contrib import admin
from .models import Productos

# Registro del modelo Producto en el admin
@admin.register(Productos)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'descripcion')  # Columnas visibles
    search_fields = ('nombre',)  # Barra de búsqueda
