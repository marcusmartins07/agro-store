from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('agrostore.usuarios.urls')),
    path('api/v1/usuarios/', include('agrostore.usuarios.urls')),
    path('api/v1/lojas/', include('agrostore.lojas.urls')),
    path('api/v1/produtos/', include('agrostore.produtos.urls')),
    path('api/v1/carrinhos/', include('agrostore.carrinhos.urls')),
    path('api/v1/pedidos/', include('agrostore.pedidos.urls')),
    path('api/v1/favoritos/', include('agrostore.favoritos.urls')),
    path('api/v1/avaliacoes/', include('agrostore.avaliacoes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
