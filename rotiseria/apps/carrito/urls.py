from django.urls import path
from .views import CarritoListView, AgregarCantidadProductoView, EliminarProductoView

app_name = 'carrito'

urlpatterns = [
    # Vista principal del carrito
    path('', CarritoListView.as_view(), name='carrito_list'),

    # Agregar un producto al carrito seleccionando la cantidad
    path('agregar/<int:pk>/', AgregarCantidadProductoView.as_view(), name='agregar_producto'),

    # Eliminar un producto del carrito
    path('eliminar/<int:pk>/', EliminarProductoView.as_view(), name='eliminar_producto'),
]
