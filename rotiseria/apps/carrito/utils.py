import mercadopago
import json
import os
from django.conf import settings
# SDK de Mercado Pago (configurado con tu Access Token)
def crear_preferencia(carrito):
    """
    Crea una preferencia en Mercado Pago basada en los productos del carrito.
    """
    # Token de acceso para Mercado Pago (Cambiar a un entorno seguro al implementar)
    # Usa una variable de entorno en producción para mayor seguridad
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
        "success": "https://a1de-181-110-191-84.ngrok-free.app/carrito/pago-exitoso/",  # URL pública
        "failure": "https://a1de-181-110-191-84.ngrok-free.app/carrito/pago-fallido/",  # URL pública
        "pending": "https://a1de-181-110-191-84.ngrok-free.app/carrito/pago-pendiente/"  # URL pública
    },
    "auto_return": "approved",  # Redirige automáticamente si el pago se aprueba
    "notification_url": "https://a1de-181-110-191-84.ngrok-free.app/carrito/notificacion/",  # URL pública
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


# apps/carrito/utils.py

def procesar_notificacion_pago(datos):
    """
    Procesa la notificación enviada por Mercado Pago y registra el pedido.
    """
    try:
        # Lógica para procesar la notificación (asegúrate de que los datos sean correctos)
        print("Datos de la notificación recibida:", datos)

        # Verifica el estado del pago aquí (por ejemplo: "approved")
        if "status" in datos and datos["status"] == "approved":
            # Agregar lógica de registro de pedido
            print("Pago aprobado")
        else:
            print("El pago no fue aprobado")

    except Exception as e:
        print(f"Error procesando notificación: {e}")
        raise  # Vuelve a lanzar la excepción si es necesario
