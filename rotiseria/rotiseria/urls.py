
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('productos/', include(('apps.productos.urls', 'productos'), namespace='productos')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  
