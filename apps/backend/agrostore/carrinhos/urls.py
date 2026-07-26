from rest_framework.routers import DefaultRouter
from .views import CarrinhoViewSet

router = DefaultRouter()
router.register(r'', CarrinhoViewSet, basename='carrinho')

urlpatterns = router.urls