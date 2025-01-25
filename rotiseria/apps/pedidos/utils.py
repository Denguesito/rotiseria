from django.core.mail import send_mail
import json

def enviar_notificacion_email(pedido):
    """Envía una notificación de pedido confirmado por correo electrónico al administrador."""
    asunto = "Nuevo pedido confirmado"
    mensaje = (
        f"Se ha recibido un nuevo pedido pagado:\n"
        f"Cliente: {pedido.cliente_nombre}\n"
        f"Teléfono: {pedido.cliente_telefono}\n"
        f"Detalles del pedido:\n"
        + "\n".join([
            f"- {item.producto.nombre} x{item.cantidad} (${item.producto.precio * item.cantidad})"
            for item in pedido.carrito.items.all()
        ])
    )
    
    destinatarios = ["denguesito2013@gmail.com"]

    try:
        send_mail(
            subject=asunto,
            message=mensaje,
            from_email="denguesito2013@gmail.com",  # Tu correo como remitente
            recipient_list=destinatarios,
            fail_silently=False,
        )
        print("Correo enviado con éxito al administrador.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def procesar_notificacion_pago(datos):
    """
    Procesa la notificación de pago recibida desde Mercado Pago y realiza las acciones necesarias,
    como enviar la notificación por correo electrónico al administrador.
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
            # Aquí, 'datos' puede contener los detalles del pago y del pedido, por lo que puedes extraerlos de la notificación.
            pedido = datos.get("pedido")  # O la forma en que se almacenan los datos del pedido en 'datos'

            # Llamar a la función de notificación por correo
            if pedido:
                enviar_notificacion_email(pedido)  # Envía el correo al administrador con la información del pedido
            else:
                print("No se encontraron detalles del pedido en la notificación.")
            
            print("Notificación procesada y enviada.")
        else:
            print(f"Estado del pago: {datos.get('status')}")
            print("El pago no fue aprobado.")
    
    except Exception as e:
        print(f"Error procesando la notificación: {e}")