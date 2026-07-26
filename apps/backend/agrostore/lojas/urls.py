from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LojaViewSet, MinhaLojaView

router = DefaultRouter()
router.register('lojas', LojaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('me/', MinhaLojaView.as_view()),  # ← nova rota
]