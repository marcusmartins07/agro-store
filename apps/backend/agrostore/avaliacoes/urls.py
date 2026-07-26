from rest_framework.routers import DefaultRouter
from .views import AvaliacaoViewSet

router = DefaultRouter()
router.register(r'', AvaliacaoViewSet, basename='avaliacoes')

urlpatterns = router.urls