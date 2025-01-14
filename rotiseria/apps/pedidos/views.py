from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import Pedido
from apps.carrito.models import CarritoItem
from .utils import enviar_notificacion_whatsapp, procesar_notificacion_pago
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import EstadisticaVenta
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.core.serializers.json import DjangoJSONEncoder
import json

class CrearPedidoView(View):
    """Crea un pedido y marca su estado como 'pagado'."""

    def post(self, request, carrito_id):
        # Obtén el carrito relacionado con el usuario
        carrito = CarritoItem.objects.filter(carrito__id=carrito_id).first()
        
        if not carrito:
            messages.error(request, "Carrito no encontrado.")
            return redirect('index')  # Redirige a la página principal
        
        # Crear el pedido sin necesidad de 'estado', Mercado Pago maneja el estado
        pedido = Pedido.objects.create(
            carrito=carrito,
            cliente_nombre=carrito.carrito.cliente_nombre,
            cliente_telefono=carrito.carrito.cliente_telefono
        )
        
        # Enviar la notificación de WhatsApp al administrador
        enviar_notificacion_whatsapp(pedido)
        
        # Actualizar estadísticas de ventas
        total_ventas = sum(item.producto.precio * item.cantidad for item in carrito.items.all())
        
        # Calcular fecha de la semana y mes actual
        fecha_actual = datetime.today().date()
        fecha_inicio_semana = fecha_actual - timedelta(days=fecha_actual.weekday())
        fecha_inicio_mes = fecha_actual.replace(day=1)
        
        # Actualizar las estadísticas de ventas semanales y mensuales
        EstadisticaVenta.actualizar_estadisticas(fecha_inicio_semana, fecha_actual, total_ventas)
        EstadisticaVenta.actualizar_estadisticas(fecha_inicio_mes, fecha_actual, total_ventas)
        
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
    """Recibe y procesa las notificaciones de pago de Mercado Pago."""

    def post(self, request):
        try:
            # Datos recibidos de Mercado Pago
            datos = request.POST

            # Procesar la notificación de pago
            if procesar_notificacion_pago(datos):
                # Actualizar las estadísticas de ventas
                pedido_id = datos.get('order_id')
                pedido = Pedido.objects.get(id=pedido_id)
                carrito = pedido.carrito
                total_ventas = sum(item.producto.precio * item.cantidad for item in carrito.items.all())
                
                # Calcular fecha de la semana y mes actual
                fecha_actual = datetime.today().date()
                fecha_inicio_semana = fecha_actual - timedelta(days=fecha_actual.weekday())
                fecha_inicio_mes = fecha_actual.replace(day=1)
                
                # Actualizar las estadísticas de ventas semanales y mensuales
                EstadisticaVenta.actualizar_estadisticas(fecha_inicio_semana, fecha_actual, total_ventas)
                EstadisticaVenta.actualizar_estadisticas(fecha_inicio_mes, fecha_actual, total_ventas)

                return JsonResponse({"status": "Notificación recibida y procesada correctamente"})
            else:
                return JsonResponse({"error": "El pago no fue aprobado."}, status=400)

        except Exception as e:
            return JsonResponse({"error": f"Error procesando la notificación: {e}"}, status=500)

# Aplicar el decorador a la clase entera para restringir el acceso solo a los administradores
@method_decorator(staff_member_required, name='dispatch')
class EstadisticasVentasView(View):
    def get(self, request):
        fecha_actual = datetime.today().date()

        # Obtener las estadísticas de ventas semanales y mensuales
        ventas_semanales = EstadisticaVenta.ventas_semanales()  # Asegúrate de que esta función esté definida en tu modelo
        ventas_mensuales = EstadisticaVenta.ventas_mensuales()  # Asegúrate de que esta función esté definida en tu modelo

        # Preprocesar datos para los gráficos
        datos_semanales = {
            'fechas': [f"{v.fecha_inicio} - {v.fecha_fin}" for v in ventas_semanales],
            'ventas': [float(v.total_ventas) for v in ventas_semanales]
        }
        datos_mensuales = {
            'fechas': [f"{v.fecha_inicio} - {v.fecha_fin}" for v in ventas_mensuales],
            'ventas': [float(v.total_ventas) for v in ventas_mensuales]
        }

        context = {
            'ventas_semanales': ventas_semanales,
            'ventas_mensuales': ventas_mensuales,
            'fecha_actual': fecha_actual,
            'datos_semanales': json.dumps(datos_semanales, cls=DjangoJSONEncoder),
            'datos_mensuales': json.dumps(datos_mensuales, cls=DjangoJSONEncoder),
        }

        return render(request, 'pedidos/estadisticas_ventas.html', context)