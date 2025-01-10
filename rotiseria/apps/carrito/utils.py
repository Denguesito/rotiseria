import mercadopago
import json

def crear_preferencia(carrito):
    """Crea una preferencia en Mercado Pago para el carrito."""
    sdk = mercadopago.SDK("TU_ACCESS_TOKEN_AQUÍ")

    items = [
        {
            "title": item.producto.nombre,
            "quantity": item.cantidad,
            "unit_price": float(item.producto.precio),
        }
        for item in carrito.items.all()
    ]

    preferencia = {
        "items": items,
        "back_urls": {
            "success": "http://127.0.0.1:8000/carrito/pago-exitoso/",
            "failure": "http://127.0.0.1:8000/carrito/pago-fallido/",
            "pending": "http://127.0.0.1:8000/carrito/pago-pendiente/",
        },
        "auto_return": "approved",
    }

    try:
        response = sdk.preference().create(preferencia)
        return response["response"]["init_point"]
    except Exception as e:
        print(f"Error al crear la preferencia: {e}")
        return None


def procesar_notificacion_pago(datos):
    """Procesa la notificación de Mercado Pago para registrar el pedido."""
    try:
        # Aquí puedes procesar el JSON enviado por Mercado Pago
        print("Datos de la notificación recibida:", json.dumps(datos, indent=4))
        # Realiza las validaciones y crea el pedido en la base de datos
    except Exception as e:
        print(f"Error procesando notificación: {e}")
