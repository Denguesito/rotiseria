from django.urls import path
from .views import ListaProductosView, DetallesProductoView

app_name = 'productos'

urlpatterns = [
    path('', ListaProductosView.as_view(), name='lista'),
    path('<int:pk>/', DetallesProductoView.as_view(), name='detalles'),
]
