from datetime import datetime, time
from .models import Carrito

def horario_atencion(request):
    ahora = datetime.now().time()
    hora_apertura = time(10, 0)  # 10:00 AM
    hora_cierre = time(0, 30)    # 00:30 AM del siguiente día

    if hora_apertura <= ahora or ahora < hora_cierre:
        estado = {
            'estado_rotiseria': 'abierto',
            'color_estado': 'green'
        }
    else:
        estado = {
            'estado_rotiseria': 'cerrado',
            'color_estado': 'red'
        }
    
    print("Estado: ", estado)  # Agrega esta línea para ver el valor en la consola
    return estado

def total_productos_carrito(request):
    carrito_id = request.session.get('carrito_id', None)
    total_productos = 0
    if carrito_id:
        try:
            carrito = Carrito.objects.get(id=carrito_id)
            total_productos = carrito.total_items()
        except Carrito.DoesNotExist:
            pass
    return {'total_productos': total_productos}
