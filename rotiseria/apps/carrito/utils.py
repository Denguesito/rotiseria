import mercadopago
import json

# SDK de Mercado Pago (configurado con tu Access Token)
def crear_preferencia(carrito):
    """
    Crea una preferencia en Mercado Pago basada en los productos del carrito.
    """
    # Token de acceso para Mercado Pago (Cambiar a un entorno seguro al implementar)
    # Usa una variable de entorno en producción para mayor seguridad
    sdk = mercadopago.SDK("TU_ACCESS_TOKEN_AQUÍ")  # Cambiar por el token real

    # Generar la lista de ítems desde el carrito
    items = [
        {
            "title": item.producto.nombre,        # Nombre del producto
            "quantity": item.cantidad,           # Cantidad de unidades
            "unit_price": float(item.producto.precio),  # Precio unitario
        }
        for item in carrito.items.all()
    ]

    # Configurar la preferencia
    preferencia = {
        "items": items,
        "back_urls": {
            # Cambiar estas URLs al dominio real al subir al servidor
            "success": "http://127.0.0.1:8000/carrito/pago-exitoso/",   # Pruebas locales
            "failure": "http://127.0.0.1:8000/carrito/pago-fallido/",  # Pruebas locales
            "pending": "http://127.0.0.1:8000/carrito/pago-pendiente/" # Pruebas locales
        },
        "auto_return": "approved",  # Redirige automáticamente si el pago se aprueba
        "notification_url": "http://127.0.0.1:8000/carrito/notificacion/",  # Cambiar en producción
    }

    try:
        # Llamar a la API de Mercado Pago para crear la preferencia
        response = sdk.preference().create(preferencia)
        return response["response"]["init_point"]  # URL para redirigir al cliente
    except Exception as e:
        print(f"Error al crear la preferencia: {e}")
        return None


def procesar_notificacion_pago(datos):
    """
    Procesa la notificación enviada por Mercado Pago y registra el pedido.
    """
    try:
        # Para depurar, imprime los datos recibidos
        print("Datos de la notificación recibida:", json.dumps(datos, indent=4))

        # Ejemplo de validación inicial:
        # Puedes verificar el status del pago, el ID del pedido, entre otros.
        if "id" in datos:
            # Aquí podrías buscar el pago en Mercado Pago y verificar su estado
            # Por ejemplo: verificar si es 'approved'
            print(f"ID de pago recibido: {datos['id']}")
        
        # Agrega lógica para registrar el pedido en la base de datos aquí
        # ...
        print("Notificación procesada exitosamente.")
    except Exception as e:
        print(f"Error procesando notificación: {e}")
