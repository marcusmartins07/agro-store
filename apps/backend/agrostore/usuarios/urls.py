from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CadastroClienteView,
    ConfirmacaoRedefinicaoSenhaView,
    LoginView,
    MeView,
    MinhaFotoView,
    SolicitacaoRedefinicaoSenhaView,
)


urlpatterns = [
    path('cadastro/', CadastroClienteView.as_view(), name='cadastro-cliente'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('me/foto/', MinhaFotoView.as_view(), name='me-foto'),
    path('redefinir-senha/', SolicitacaoRedefinicaoSenhaView.as_view(), name='redefinir-senha'),
    path('redefinir-senha/confirmar/', ConfirmacaoRedefinicaoSenhaView.as_view(), name='redefinir-senha-confirmar'),
]
