from rest_framework.routers import DefaultRouter
from .views import ProdutoViewSet, PrecoProdutoViewSet, CategoriaViewSet, ImagemProdutoViewSet

router = DefaultRouter()
router.register("categorias", CategoriaViewSet, basename="categoria")
router.register(r'precos', PrecoProdutoViewSet, basename='preco-produto')
router.register(r'(?P<produto_pk>\d+)/imagens', ImagemProdutoViewSet, basename='imagem-produto')
router.register(r'', ProdutoViewSet)

urlpatterns = router.urls
