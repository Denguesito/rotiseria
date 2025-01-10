from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import Pedido
from apps.carrito.models import CarritoItem
from .utils import enviar_notificacion_whatsapp
from django.http import JsonResponse

class CrearPedidoView(View):
    """Crea un pedido y marca su estado como 'pagado'."""

    def post(self, request, carrito_id):
        # Obtén el carrito relacionado con el usuario
        carrito = CarritoItem.objects.filter(carrito__id=carrito_id).first()
        
        if not carrito:
            messages.error(request, "Carrito no encontrado.")
            return redirect('index')  # Redirige a la página principal
        
        # Crear el pedido y marcarlo como 'pagado'
        pedido = Pedido.objects.create(
            carrito=carrito,
            cliente_nombre=carrito.carrito.cliente_nombre,
            cliente_telefono=carrito.carrito.cliente_telefono,
            estado='pagado'
        )
        
        # Enviar la notificación de WhatsApp al administrador
        enviar_notificacion_whatsapp(pedido)
        
        # Mensaje de éxito y redirección
        messages.success(request, "Pago confirmado. Pedido realizado con éxito.")
        return redirect('confirmacion_pedido', pedido_id=pedido.id)

class ConfirmacionPedidoView(View):
    """Muestra la confirmación del pedido después del pago."""

    def get(self, request, pedido_id):
        pedido = Pedido.objects.filter(id=pedido_id).first()
        
        if not pedido:
            messages.error(request, "Pedido no encontrado.")
            return redirect('index')
        
        return render(request, 'pedidos/confirmacion_pedido.html', {'pedido': pedido})

class NotificacionPagoView(View):
    """Recibe y procesa las notificaciones de Mercado Pago."""

    def post(self, request):
        try:
            # Aquí debes procesar la notificación desde Mercado Pago
            # Esto depende de la estructura de los datos enviados por Mercado Pago.
            # Procesar la notificación del pago:
            datos = request.POST
            # Actualizar el estado del pedido en la base de datos
            # Aquí puedes realizar las verificaciones necesarias con la API de MP.

            # Suponiendo que ya tienes un ID de pedido para actualizar
            pedido_id = datos.get('order_id')
            pedido = Pedido.objects.get(id=pedido_id)
            pedido.estado = 'pagado'
            pedido.save()

            # Enviar la notificación por WhatsApp
            enviar_notificacion_whatsapp(pedido)

            return JsonResponse({"status": "Notificación recibida y procesada correctamente"})
        except Exception as e:
            return JsonResponse({"error": f"Error procesando la notificación: {e}"}, status=500)
