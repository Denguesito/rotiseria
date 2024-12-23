from django.urls import path
from .views import CarritoListView, AgregarProductoView, EliminarProductoView

app_name = 'carrito'

urlpatterns = [
    path('', CarritoListView.as_view(), name='carrito_list'),
    path('agregar/', AgregarProductoView.as_view(), name='agregar_producto'),
    path('eliminar/<int:pk>/', EliminarProductoView.as_view(), name='eliminar_producto'),
]
