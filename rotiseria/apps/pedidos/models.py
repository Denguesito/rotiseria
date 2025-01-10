from django.db import models
from apps.carrito.models import Carrito
from datetime import datetime, timedelta

class Pedido(models.Model):
    carrito = models.OneToOneField(Carrito, related_name='pedido', on_delete=models.CASCADE)
    cliente_nombre = models.CharField(max_length=255)
    cliente_telefono = models.CharField(max_length=20)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.carrito}"

class EstadisticaVenta(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    total_ventas = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Total de ventas en esa semana o mes
    
    def __str__(self):
        return f"Ventas del {self.fecha_inicio} al {self.fecha_fin}: ${self.total_ventas}"

    @classmethod
    def actualizar_estadisticas(cls, fecha_inicio, fecha_fin, total_ventas):
        # Aquí se puede actualizar las estadísticas de ventas de una semana o mes
        estadistica, created = cls.objects.get_or_create(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
        estadistica.total_ventas += total_ventas
        estadistica.save()

    @classmethod
    def ventas_semanales(cls):
        """Retorna las ventas de la última semana."""
        fecha_fin = datetime.today().date()
        fecha_inicio = fecha_fin - timedelta(days=7)
        return cls.objects.filter(fecha_inicio__gte=fecha_inicio, fecha_fin__lte=fecha_fin)

    @classmethod
    def ventas_mensuales(cls):
        """Retorna las ventas del mes actual."""
        fecha_fin = datetime.today().date()
        fecha_inicio = fecha_fin.replace(day=1)  # Primer día del mes
        return cls.objects.filter(fecha_inicio__gte=fecha_inicio, fecha_fin__lte=fecha_fin)
