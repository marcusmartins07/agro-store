from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CadastroClienteView, LoginView, MeView


urlpatterns = [
    path('cadastro/', CadastroClienteView.as_view(), name='cadastro-cliente'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
]
