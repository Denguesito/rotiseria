from twilio.rest import Client
import json

def enviar_notificacion_whatsapp(pedido):
    """Envía la notificación de pago confirmado al administrador (usando el mismo número para enviar y recibir)."""
    # SID de la cuenta de Twilio y token de autenticación
    account_sid = 'your_account_sid'  # Tu SID de cuenta Twilio
    auth_token = 'your_auth_token'    # Tu token de autenticación Twilio

    # Crear un cliente Twilio con las credenciales
    client = Client(account_sid, auth_token)

    # Mensaje que se enviará al administrador
    mensaje_admin = f"Nuevo pedido confirmado y pagado:\nDetalles: {pedido}"

    # Usar el mismo número de Twilio tanto para 'from' como para 'to'
    try:
        # Enviar la notificación al administrador
        client.messages.create(
            body=mensaje_admin,  # Cuerpo del mensaje
            from_='whatsapp:+14155238886',  # Número de WhatsApp Twilio (sandbox o propio)
            to='whatsapp:+14155238886'  # Usar el mismo número para el administrador
        )
        print("Notificación enviada correctamente al administrador.")
    except Exception as e:
        print(f"Error al enviar la notificación: {e}")

def procesar_notificacion_pago(datos):
    """
    Procesa la notificación de pago recibida desde Mercado Pago y realiza las acciones necesarias,
    como enviar la notificación por WhatsApp al administrador.
    """
    try:
        # Para depurar, imprime los datos recibidos
        print("Datos de la notificación recibida:", json.dumps(datos, indent=4))

        # Ejemplo de validación: Verificar que el pago ha sido aprobado
        if datos.get("status") == "approved":
            print("Pago aprobado, procesando el pedido.")

            # Aquí deberías realizar acciones adicionales, como actualizar el estado del pedido en tu base de datos,
            # o notificar al administrador que el pago ha sido confirmado.
            
            # Supongamos que 'pedido' es el objeto que contiene la información del pedido.
            # Llama a la función de notificación
            enviar_notificacion_whatsapp(datos)
            print("Notificación procesada y enviada.")
        else:
            print(f"Estado del pago: {datos.get('status')}")
            print("El pago no fue aprobado.")
    
    except Exception as e:
        print(f"Error procesando la notificación: {e}")
