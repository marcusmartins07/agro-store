from rest_framework.routers import DefaultRouter
from .views import ProdutoViewSet, PrecoProdutoViewSet, CategoriaViewSet

router = DefaultRouter()
router.register("categorias", CategoriaViewSet, basename="categoria")
router.register(r'precos', PrecoProdutoViewSet)
router.register(r'', ProdutoViewSet)

urlpatterns = router.urls