from django.db import transaction
from django.db.models import Prefetch, prefetch_related_objects
from rest_framework import status, viewsets
from rest_framework.exceptions import APIException, Throttled
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from agrostore.main.imagens import nome_gerenciado, remover_arquivo_apos_commit
from . import redefinicao_senha
from . import telefones as servico_telefones
from .models import Telefone, TipoTelefone
from .serializers import (
    PASTA_FOTO_USUARIO,
    CadastroClienteSerializer,
    ConfirmacaoRedefinicaoSenhaSerializer,
    LoginSerializer,
    SolicitacaoRedefinicaoSenhaSerializer,
    TelefoneSerializer,
    TipoTelefoneSerializer,
    UsuarioAtualizacaoSerializer,
    UsuarioPerfilSerializer,
    validar_nova_senha,
)


def dados_perfil(usuario, request):
    # Carrega os telefones com o tipo em uma única consulta, evitando uma consulta por telefone em tipo_descricao.
    prefetch_related_objects([usuario], Prefetch('telefones', queryset=Telefone.objects.select_related('tipo')))
    return UsuarioPerfilSerializer(usuario, context={'request': request}).data


def resposta_autenticacao(user, request, response_status=200):
    refresh = RefreshToken.for_user(user)
    return Response(
        {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'usuario': dados_perfil(user, request),
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
        return Response(dados_perfil(request.user, request))

    def patch(self, request):
        campos_permitidos = set(UsuarioAtualizacaoSerializer.Meta.fields)
        campos_invalidos = set(request.data.keys()) - campos_permitidos
        if campos_invalidos:
            return Response(
                {"detail": "Somente nome, e-mail, data de nascimento, gênero e foto de perfil podem ser alterados no perfil. "
                           "Os telefones são gerenciados em /me/telefones/."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = UsuarioAtualizacaoSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(dados_perfil(serializer.save(), request))


class RegraTelefoneRecusada(APIException):
    """Regra da RN-021 recusada pelo serviço de telefones; responde 400 com detail em texto, como o resto da API."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'regra_telefone'


class TelefoneViewSet(viewsets.ModelViewSet):
    """Telefones do usuário autenticado (RN-021); telefone de outro usuário responde 404."""

    serializer_class = TelefoneSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        return Telefone.objects.filter(usuario=self.request.user).select_related('tipo')

    def perform_create(self, serializer):
        dados = serializer.validated_data
        serializer.instance = self._aplicar_regra(
            servico_telefones.criar_telefone,
            self.request.user,
            dados['numero'],
            dados['tipo'],
            e_principal=dados.get('e_principal', False),
        )

    def perform_update(self, serializer):
        dados = serializer.validated_data
        serializer.instance = self._aplicar_regra(
            servico_telefones.atualizar_telefone,
            serializer.instance,
            numero=dados.get('numero'),
            tipo=dados.get('tipo'),
            e_principal=dados.get('e_principal'),
        )

    def perform_destroy(self, instance):
        self._aplicar_regra(servico_telefones.excluir_telefone, instance)

    def _aplicar_regra(self, operacao, *args, **kwargs):
        try:
            return operacao(*args, **kwargs)
        except servico_telefones.RegraTelefoneViolada as erro:
            raise RegraTelefoneRecusada(str(erro)) from erro


class TipoTelefoneListView(ListAPIView):
    """Tipos fixos de telefone (RN-021), públicos porque o cadastro é feito sem login."""

    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = TipoTelefoneSerializer
    pagination_class = None
    queryset = TipoTelefone.objects.order_by('id')


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
