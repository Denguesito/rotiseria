from .views import obtener_carrito_activo

class CarritoMiddleware:
    """Middleware para asegurar que cada solicitud tenga acceso a un carrito activo."""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Llamar a la función para obtener el carrito activo
        carrito = obtener_carrito_activo(request)

        # Hacer disponible el carrito en el contexto de la solicitud
        request.carrito = carrito

        # Llamar a la vista
        response = self.get_response(request)

        return response
