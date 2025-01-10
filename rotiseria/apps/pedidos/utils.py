# utils.py en la app 'pedidos'
from twilio.rest import Client

def enviar_notificacion_whatsapp(pedido):
    """Envía la notificación por WhatsApp al cliente y al administrador."""
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    client = Client(account_sid, auth_token)
    
    mensaje_cliente = f"¡Tu pedido ha sido confirmado!\nDetalles: {pedido}"
    mensaje_admin = f"Nuevo pedido recibido: {pedido}"
    
    # Notificación al cliente
    client.messages.create(
        body=mensaje_cliente,
        from_='whatsapp:+14155238886',
        to=f'whatsapp:{pedido.cliente_telefono}'
    )
    
    # Notificación al administrador
    client.messages.create(
        body=mensaje_admin,
        from_='whatsapp:+14155238886',
        to='whatsapp:+1234567890'  # Número de administrador
    )
