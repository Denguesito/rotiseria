import mercadopago
import os
from django.conf import settings
import json

def crear_preferencia(carrito):
    """
    Crea una preferencia en Mercado Pago basada en los productos del carrito.
    """
    # Token de acceso para Mercado Pago desde variable de entorno (ajusta según sea necesario)
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
    
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
            "success": "https://www.tudominio.com/carrito/pago-exitoso/",  # URL pública en producción
            "failure": "https://www.tudominio.com/carrito/pago-fallido/",  # URL pública en producción
            "pending": "https://www.tudominio.com/carrito/pago-pendiente/"  # URL pública en producción
        },
        "auto_return": "approved",  # Redirige automáticamente si el pago se aprueba
        "notification_url": "https://www.tudominio.com/carrito/notificacion/",  # URL pública en producción
    }

    try:
        # Llamar a la API de Mercado Pago para crear la preferencia
        response = sdk.preference().create(preferencia)
        
        # Verificamos si la respuesta es exitosa
        if response["status"] == 201:
            # La preferencia se creó correctamente
            return response["response"]["init_point"]  # URL para redirigir al cliente
        else:
            print(f"Error en la respuesta de Mercado Pago: {response}")
            return None
    except mercadopago.exceptions.MPException as e:
        # Aquí podemos capturar más detalles sobre el error
        print(f"Error al crear la preferencia: {e}")
        print(f"Detalles del error: {e.message}")
        return None


def procesar_notificacion_pago(datos):
    """
    Procesa la notificación enviada por Mercado Pago y registra el pedido.
    """
    try:
        # Lógica para procesar la notificación (asegúrate de que los datos sean correctos)
        print("Datos de la notificación recibida:", json.dumps(datos, indent=4))

        # Verifica el estado del pago aquí (por ejemplo: "approved")
        if "status" in datos and datos["status"] == "approved":
            # Agregar lógica de registro de pedido
            print("Pago aprobado, procesando el pedido...")
            # Aquí puedes agregar la lógica para guardar el pedido y marcarlo como confirmado
        else:
            print(f"El pago no fue aprobado. Estado: {datos.get('status')}")
            # Si es necesario, puedes agregar lógica para manejar estados "pending" o "rejected"
    
    except Exception as e:
        print(f"Error procesando notificación: {e}")
        raise  # Vuelve a lanzar la excepción si es necesario
