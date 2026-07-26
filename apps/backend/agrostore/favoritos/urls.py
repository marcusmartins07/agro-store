from rest_framework.routers import DefaultRouter
from .views import FavoritoViewSet

router = DefaultRouter()
router.register(r'', FavoritoViewSet, basename='favoritos')

urlpatterns = router.urls