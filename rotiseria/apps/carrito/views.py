from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, View, DeleteView
from django.contrib import messages
from .models import Carrito, CarritoItem
from .forms import CarritoForm, AgregarCantidadProductoForm
from apps.productos.models import Productos


def obtener_carrito_activo(request):
    carrito_id = request.session.get('carrito_id', None)
    if carrito_id:
        # Si ya hay un carrito en la sesión, lo buscamos
        return get_object_or_404(Carrito, id=carrito_id)
    else:
        # Si no hay un carrito, creamos uno nuevo, sin valores por defecto
        carrito = Carrito.objects.create(cliente_nombre="", cliente_telefono="")
        # Guardamos el ID del carrito en la sesión
        request.session['carrito_id'] = carrito.id
        return carrito

class CarritoListView(ListView):
    """Muestra el carrito y los productos añadidos."""
    model = CarritoItem
    template_name = 'carrito/carrito_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        # Obtén el carrito activo desde request.carrito
        carrito = self.request.carrito
        return carrito.items.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtén el carrito activo desde request.carrito
        carrito = self.request.carrito
        
        # Crear el formulario vacío (sin valores predeterminados)
        context['form'] = CarritoForm()  # No pasa 'instance=carrito'
        
        # Añadir el carrito al contexto
        context['carrito'] = carrito
        
        # Contar la cantidad total de productos en el carrito
        total_productos = sum(item.cantidad for item in carrito.items.all())
        context['total_productos'] = total_productos

        return context


class AgregarCantidadProductoView(View):
    """Vista para seleccionar la cantidad de un producto antes de agregarlo al carrito."""
    
    def get(self, request, pk):
        producto = get_object_or_404(Productos, pk=pk)
        form = AgregarCantidadProductoForm()  # No es necesario pasar 'producto' al formulario aquí
        return render(request, 'carrito/agregar_cantidad.html', {'form': form, 'producto': producto})

    def post(self, request, pk):
        producto = get_object_or_404(Productos, pk=pk)
        form = AgregarCantidadProductoForm(request.POST)

        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            carrito = obtener_carrito_activo(request)  # Función para obtener el carrito activo
            
            carrito_item, creado = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)

            if not creado:
                carrito_item.cantidad += cantidad
            else:
                carrito_item.cantidad = cantidad

            carrito_item.save()
            messages.success(request, f"Se agregó {producto.nombre} al carrito.")
            return redirect('index')  # Redirige a la página principal o la vista que desees

        messages.error(request, "No se pudo agregar el producto al carrito.")
        return render(request, 'carrito/agregar_cantidad.html', {'form': form, 'producto': producto})

class EliminarProductoView(DeleteView):
    """Elimina un producto del carrito."""
    model = CarritoItem
    template_name = 'carrito/eliminar_producto.html'

    def get_success_url(self):
        messages.success(self.request, "Producto eliminado del carrito.")
        return reverse_lazy('index')
