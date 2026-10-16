from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import Throttled
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from agrostore.main.imagens import nome_gerenciado, remover_arquivo_apos_commit
from . import redefinicao_senha
from .serializers import (
    PASTA_FOTO_USUARIO,
    CadastroClienteSerializer,
    ConfirmacaoRedefinicaoSenhaSerializer,
    LoginSerializer,
    SolicitacaoRedefinicaoSenhaSerializer,
    UsuarioAtualizacaoSerializer,
    UsuarioPerfilSerializer,
    validar_nova_senha,
)


def resposta_autenticacao(user, request, response_status=200):
    refresh = RefreshToken.for_user(user)
    return Response(
        {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'usuario': UsuarioPerfilSerializer(user, context={'request': request}).data,
        },
        status=response_status,
    )


class CadastroClienteView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CadastroClienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return resposta_autenticacao(serializer.save(), request, 201)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return resposta_autenticacao(serializer.validated_data['user'], request)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UsuarioPerfilSerializer(request.user, context={'request': request}).data)

    def patch(self, request):
        campos_permitidos = set(UsuarioAtualizacaoSerializer.Meta.fields)
        campos_invalidos = set(request.data.keys()) - campos_permitidos
        if campos_invalidos:
            return Response(
                {"detail": "Somente nome, e-mail, celular, data de nascimento, gênero e foto de perfil podem ser alterados no perfil."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = UsuarioAtualizacaoSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(UsuarioPerfilSerializer(serializer.save(), context={'request': request}).data)


class MinhaFotoView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        usuario = request.user
        nome_anterior = usuario.foto_perfil.name
        # Valor vazio ou fora do padrão gerado é exibido como sem foto; o dado é preservado.
        if not nome_gerenciado(nome_anterior, PASTA_FOTO_USUARIO):
            return Response({"detail": "Você não possui foto de perfil."}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            usuario.foto_perfil = ''
            usuario.save(update_fields=['foto_perfil'])
            remover_arquivo_apos_commit(usuario.foto_perfil.storage, nome_anterior, PASTA_FOTO_USUARIO)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RedefinicaoSenhaBaseView(APIView):
    """Endpoints públicos da RN-020: sem autenticação JWT, para o limite contar sempre por IP."""

    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]

    def throttled(self, request, wait):
        excecao = Throttled(detail=redefinicao_senha.MENSAGEM_LIMITE)
        excecao.wait = wait
        raise excecao


class SolicitacaoRedefinicaoSenhaView(RedefinicaoSenhaBaseView):
    throttle_scope = 'redefinicao_senha'

    def post(self, request):
        serializer = SolicitacaoRedefinicaoSenhaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        redefinicao_senha.solicitar_redefinicao(serializer.validated_data['email'])
        return Response({'detail': redefinicao_senha.MENSAGEM_SOLICITACAO})


class ConfirmacaoRedefinicaoSenhaView(RedefinicaoSenhaBaseView):
    throttle_scope = 'redefinicao_senha_confirmacao'

    def post(self, request):
        serializer = ConfirmacaoRedefinicaoSenhaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dados = serializer.validated_data
        resposta_link_invalido = Response({'detail': redefinicao_senha.MENSAGEM_LINK_INVALIDO}, status=status.HTTP_400_BAD_REQUEST)

        try:
            redefinicao = redefinicao_senha.buscar_redefinicao_valida(dados['token'])
        except redefinicao_senha.LinkRedefinicaoInvalido:
            return resposta_link_invalido

        validar_nova_senha(dados['password'], dados['password_confirmacao'], redefinicao.usuario)

        try:
            redefinicao_senha.confirmar_redefinicao(redefinicao, dados['password'])
        except redefinicao_senha.LinkRedefinicaoInvalido:
            return resposta_link_invalido
        return Response({'detail': redefinicao_senha.MENSAGEM_SUCESSO})
