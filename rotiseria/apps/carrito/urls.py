from django.urls import path
from .views import CarritoListView, AgregarCantidadProductoView, EliminarProductoView,IniciarPagoView, NotificacionPagoView

app_name = 'carrito'

urlpatterns = [
    # Vista principal del carrito
    path('', CarritoListView.as_view(), name='carrito_list'),
    # Agregar un producto al carrito seleccionando la cantidad
    path('agregar/<int:pk>/', AgregarCantidadProductoView.as_view(), name='agregar_producto'),
    # Eliminar un producto del carrito
    path('eliminar/<int:pk>/', EliminarProductoView.as_view(), name='eliminar_producto'),
    path('iniciar_pago/', IniciarPagoView.as_view(), name='iniciar_pago'),
    path('notificacion_pago/', NotificacionPagoView.as_view(), name='notificacion_pago'),

]