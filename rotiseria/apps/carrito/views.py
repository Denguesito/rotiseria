from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, View, DeleteView
from django.contrib import messages
from .models import Carrito, CarritoItem
from .forms import CarritoForm, AgregarCantidadProductoForm
from apps.productos.models import Productos
from django.http import JsonResponse
from .utils import crear_preferencia, procesar_notificacion_pago
from datetime import datetime, time


def obtener_carrito_activo(request):
    carrito_id = request.session.get('carrito_id', None)
    if carrito_id:
        return get_object_or_404(Carrito, id=carrito_id)
    else:
        carrito = Carrito.objects.create(cliente_nombre="", cliente_telefono="")
        request.session['carrito_id'] = carrito.id
        return carrito


class CarritoListView(ListView):
    model = CarritoItem
    template_name = 'carrito/carrito_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        carrito = self.request.carrito
        return carrito.items.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrito = self.request.carrito
        context['form'] = CarritoForm()
        context['carrito'] = carrito
        context['total_productos'] = sum(item.cantidad for item in carrito.items.all())
        return context


class AgregarCantidadProductoView(View):
    def get(self, request, pk):
        producto = get_object_or_404(Productos, pk=pk)
        form = AgregarCantidadProductoForm()
        return render(request, 'carrito/agregar_cantidad.html', {'form': form, 'producto': producto})

    def post(self, request, pk):
        ahora = datetime.now().time()
        hora_apertura = time(10, 0)
        hora_cierre = time(0, 30)

        if not (hora_apertura <= ahora or ahora < hora_cierre):
            messages.error(request, "La rotisería está cerrada. No puedes agregar productos al carrito.")
            return redirect('index')

        producto = get_object_or_404(Productos, pk=pk)
        form = AgregarCantidadProductoForm(request.POST)

        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            carrito = obtener_carrito_activo(request)
            carrito_item, creado = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)

            if not creado:
                carrito_item.cantidad += cantidad
            else:
                carrito_item.cantidad = cantidad

            carrito_item.save()
            messages.success(request, f"Se agregó {producto.nombre} al carrito.")
            
            # Redirigir al índice después de agregar el producto al carrito
            return redirect('index')

        messages.error(request, "No se pudo agregar el producto al carrito.")
        return redirect('index')


class EliminarProductoView(DeleteView):
    model = CarritoItem
    template_name = 'carrito/eliminar_producto.html'

    def get_success_url(self):
        messages.success(self.request, "Producto eliminado del carrito.")
        return reverse_lazy('index')


class IniciarPagoView(View):
    def get(self, request):
        ahora = datetime.now().time()
        hora_apertura = time(20, 30)
        hora_cierre = time(0, 30)

        if not (hora_apertura <= ahora or ahora < hora_cierre):
            messages.error(request, "La rotisería está cerrada. No puedes realizar pagos en este momento.")
            return redirect('carrito:carrito_list')

        carrito = obtener_carrito_activo(request)
        init_point = crear_preferencia(carrito)

        if init_point:
            return redirect(init_point)
        else:
            return JsonResponse({"error": "No se pudo generar el pago."}, status=400)


class NotificacionPagoView(View):
    def post(self, request):
        try:
            datos = request.POST
            procesar_notificacion_pago(datos)
            return JsonResponse({"status": "Notificación recibida y procesada correctamente"})
        except Exception as e:
            return JsonResponse({"error": f"Error procesando la notificación: {e}"}, status=500)
