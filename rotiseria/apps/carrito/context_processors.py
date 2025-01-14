from datetime import datetime, time
from .models import Carrito

def horario_atencion(request):
    """
    Determina si la rotisería está abierta o cerrada según el horario de atención.
    """
    ahora = datetime.now().time()
    hora_apertura = time(20, 30)  # 8:30 PM
    hora_cierre = time(0, 30)     # 12:30 AM del siguiente día

    # Verificar si el horario actual está dentro del rango de atención
    if hora_apertura <= ahora or ahora < hora_cierre:
        estado = {
            'estado_rotiseria': 'abierto',
            'color_estado': 'success'  # Bootstrap usa "success" para color verde
        }
    else:
        estado = {
            'estado_rotiseria': 'cerrado',
            'color_estado': 'danger'  # Bootstrap usa "danger" para color rojo
        }

    # Para depuración en consola
    print("Estado actual de la rotisería:", estado)

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
