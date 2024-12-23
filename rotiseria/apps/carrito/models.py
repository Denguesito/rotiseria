from django.db import models
from apps.productos.models import Productos

class Carrito(models.Model):
    """Representa el carrito de compras activo."""
    cliente_nombre = models.CharField(max_length=100, verbose_name="Nombre del cliente")
    cliente_telefono = models.CharField(max_length=15, verbose_name="Teléfono del cliente")
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")

    def total(self):
        """Calcula el total del carrito sumando todos los subtotales de los ítems."""
        return sum(item.subtotal() for item in self.items.all())

    def total_items(self):
        """Devuelve el total de productos en el carrito."""
        return sum(item.cantidad for item in self.items.all())

    def __str__(self):
        return f"Carrito de {self.cliente_nombre} - {self.creado_en.strftime('%Y-%m-%d %H:%M:%S')}"


class CarritoItem(models.Model):
    """Representa un producto en el carrito."""
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name="en_carritos")
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")

    def subtotal(self):
        """Calcula el subtotal de este ítem."""
        return self.cantidad * self.producto.precio

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en {self.carrito}"

# Create your models here.
