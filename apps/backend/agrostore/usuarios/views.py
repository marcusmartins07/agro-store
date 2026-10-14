from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CadastroClienteSerializer, LoginSerializer, UsuarioAtualizacaoSerializer, UsuarioPerfilSerializer


def resposta_autenticacao(user, response_status=200):
    refresh = RefreshToken.for_user(user)
    return Response(
        {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'usuario': UsuarioPerfilSerializer(user).data,
        },
        status=response_status,
    )


class CadastroClienteView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CadastroClienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return resposta_autenticacao(serializer.save(), 201)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return resposta_autenticacao(serializer.validated_data['user'])


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UsuarioPerfilSerializer(request.user).data)

    def patch(self, request):
        campos_permitidos = set(UsuarioAtualizacaoSerializer.Meta.fields)
        campos_invalidos = set(request.data.keys()) - campos_permitidos
        if campos_invalidos:
            return Response(
                {"detail": "Somente nome, e-mail, celular, data de nascimento e gênero podem ser alterados no perfil."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = UsuarioAtualizacaoSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(UsuarioPerfilSerializer(serializer.save()).data)
