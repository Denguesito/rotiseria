# Generated by Django 5.1.1 on 2024-12-20 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productos',
            name='disponible',
        ),
        migrations.AddField(
            model_name='productos',
            name='categoria',
            field=models.CharField(choices=[('Pizzas', 'Pizzas'), ('Hamburguesas', 'Hamburguesas'), ('Lomitos', 'Lomitos'), ('Sandwich de milanesa', 'Sandwich de milanesa'), ('Papas fritas', 'Papas fritas')], default='Pizzas', max_length=30),
        ),
        migrations.AlterField(
            model_name='productos',
            name='descripcion',
            field=models.TextField(),
        ),
    ]
