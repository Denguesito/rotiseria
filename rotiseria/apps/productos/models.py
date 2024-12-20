from django.db import models

class Productos(models.Model):
    CATEGORIAS = [
        ('Pizzas', 'Pizzas'),
        ('Hamburguesas', 'Hamburguesas'),
        ('Lomitos', 'Lomitos'),
        ('Sandwich de milanesa', 'Sandwich de milanesa'),
        ('Papas fritas', 'Papas fritas'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=30, choices=CATEGORIAS, default='Pizzas')
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return self.nombre
