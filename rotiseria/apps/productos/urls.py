from django.urls import path
from .views import ProductoListView, ProductoDetailView

app_name = 'productos'

urlpatterns = [
    path('', ProductoListView.as_view(), name='lista_productos'),  # Lista de productos
    path('<int:pk>/', ProductoDetailView.as_view(), name='detalle_producto'),  # Detalle del producto
]
