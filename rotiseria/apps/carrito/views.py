from django.shortcuts import get_object_or_404, redirect,render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, View
from .models import Carrito, CarritoItem
from .forms import CarritoForm, AgregarProductoForm
from productos.models import Productos


class CarritoListView(ListView):
    """Muestra el carrito y los productos añadidos."""
    model = CarritoItem
    template_name = 'carrito/carrito_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        # Recuperar el carrito activo para el cliente (usamos un carrito fijo para esta implementación)
        carrito, creado = Carrito.objects.get_or_create(cliente_nombre="Cliente Temporal")
        return carrito.items.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrito, _ = Carrito.objects.get_or_create(cliente_nombre="Cliente Temporal")
        context['carrito'] = carrito
        context['form'] = CarritoForm(instance=carrito)
        return context

class AgregarProductoView(CreateView):
    """Agrega un producto al carrito."""
    model = CarritoItem
    form_class = AgregarProductoForm
    template_name = 'carrito/agregar_producto.html'

    def form_valid(self, form):
        carrito, _ = Carrito.objects.get_or_create(cliente_nombre="Cliente Temporal")
        form.instance.carrito = carrito
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('carrito:carrito_list')

class EliminarProductoView(DeleteView):
    """Elimina un producto del carrito."""
    model = CarritoItem
    template_name = 'carrito/eliminar_producto.html'

    def get_success_url(self):
        return reverse_lazy('carrito:carrito_list')

class AgregarCantidadProductoView(View):
    """Vista para seleccionar la cantidad de un producto antes de agregarlo al carrito."""
    
    def get(self, request, pk):
        """Muestra el formulario para elegir la cantidad de un producto."""
        producto = get_object_or_404(Productos, pk=pk)
        form = AgregarProductoForm(initial={'producto': producto})
        return render(request, 'carrito/agregar_cantidad.html', {'form': form, 'producto': producto})

    def post(self, request, pk):
        """Procesa la cantidad seleccionada y agrega el producto al carrito."""
        producto = get_object_or_404(Productos, pk=pk)
        form = AgregarProductoForm(request.POST)

        if form.is_valid():
            carrito, _ = Carrito.objects.get_or_create(cliente_nombre="Cliente Temporal")
            carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)

            # Si el producto ya está en el carrito, sumamos la cantidad
            if not created:
                carrito_item.cantidad += form.cleaned_data['cantidad']
            else:
                carrito_item.cantidad = form.cleaned_data['cantidad']
            
            carrito_item.save()
            
            # Redirigimos a la lista de productos
            return redirect('productos:productos_list')  # Asegúrate de que esta URL exista
        return render(request, 'carrito/agregar_cantidad.html', {'form': form, 'producto': producto})