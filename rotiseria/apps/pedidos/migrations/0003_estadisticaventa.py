# Generated by Django 5.1.1 on 2025-01-10 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0002_remove_pedido_estado_alter_pedido_carrito'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadisticaVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('total_ventas', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
    ]
