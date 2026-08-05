from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CadastroClienteSerializer, LoginSerializer, UsuarioPerfilSerializer


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
