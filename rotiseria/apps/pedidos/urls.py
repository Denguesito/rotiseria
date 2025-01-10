from django.urls import path
from .views import CrearPedidoView, ConfirmacionPedidoView, NotificacionPagoView

urlpatterns = [
    path('crear-pedido/<int:carrito_id>/', CrearPedidoView.as_view(), name='crear_pedido'),
    path('confirmacion-pedido/<int:pedido_id>/', ConfirmacionPedidoView.as_view(), name='confirmacion_pedido'),
    path('notificacion-pago/', NotificacionPagoView.as_view(), name='notificacion_pago'),
]
