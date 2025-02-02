from datetime import datetime, time
from .models import Carrito

def horario_atencion(request):
    """
    Determina si la rotisería está abierta o cerrada según el horario de atención.
    """
    ahora = datetime.now().time()
    hora_apertura = time(20, 30)  # 8:30 PM
    hora_cierre = time(00, 30)     # 12:30 AM del siguiente día

    if hora_apertura <= hora_cierre:  # Caso sin cruce de medianoche
        abierto = hora_apertura <= ahora < hora_cierre
    else:  # Caso con cruce de medianoche
        abierto = ahora >= hora_apertura or ahora < hora_cierre

    if abierto:
        estado = {
            'estado_rotiseria': 'abierto',
            'color_estado': 'success'  # Bootstrap usa "success" para color verde
        }
    else:
        estado = {
            'estado_rotiseria': 'cerrado',
            'color_estado': 'danger'  # Bootstrap usa "danger" para color rojo
        }
    return estado

def total_productos_carrito(request):
    """
    Devuelve la cantidad total de productos en el carrito activo.
    """
    carrito_id = request.session.get('carrito_id', None)
    total_productos = 0
    if carrito_id:
        try:
            carrito = Carrito.objects.get(id=carrito_id)
            total_productos = carrito.total_items()  # Asumiendo que tienes un método total_items() en Carrito
        except Carrito.DoesNotExist:
            pass
    return {'total_productos': total_productos}
