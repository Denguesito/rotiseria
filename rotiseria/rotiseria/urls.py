from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import IndexView
from apps.pedidos.admin import admin_site  

urlpatterns = [
    path('admin/', admin_site.urls),  
    path('', IndexView.as_view(), name='index'),
    path('productos/', include(('apps.productos.urls', 'productos'), namespace='productos')),
    path('carrito/', include(('apps.carrito.urls', 'carrito'), namespace='carrito')),
    path('pedidos/', include(('apps.pedidos.urls', 'pedidos'), namespace='pedidos')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
