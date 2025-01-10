from django.db import models
from apps.carrito.models import CarritoItem

class Pedido(models.Model):
    carrito = models.ForeignKey(CarritoItem, related_name='pedidos', on_delete=models.CASCADE)
    cliente_nombre = models.CharField(max_length=255)
    cliente_telefono = models.CharField(max_length=20)
    estado = models.CharField(max_length=10, default='pagado')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.estado}"

    def get_estado_display(self):
        return self.estado.capitalize()

