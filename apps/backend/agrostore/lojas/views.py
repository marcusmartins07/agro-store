from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Loja
from .serializers import LojaSerializer


class LojaViewSet(viewsets.ModelViewSet):
    queryset = Loja.objects.select_related('proprietario').all()
    serializer_class = LojaSerializer
    http_method_names = ['get', 'post', 'patch']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(proprietario=self.request.user)


class MinhaLojaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        loja = Loja.objects.filter(proprietario=request.user).first()

        if not loja:
            return Response({"detail": "Você não possui uma loja cadastrada."}, status=404)

        serializer = LojaSerializer(loja)
        return Response(serializer.data)

    def patch(self, request):
        loja = Loja.objects.filter(proprietario=request.user).first()
        if not loja:
            return Response({"detail": "Você não possui uma loja cadastrada."}, status=status.HTTP_404_NOT_FOUND)

        campos_permitidos = {'descricao', 'ativa'}
        campos_enviados = set(request.data.keys())
        campos_invalidos = campos_enviados - campos_permitidos
        if campos_invalidos:
            return Response(
                {"detail": "Somente descrição e status da loja podem ser alterados nesta área."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = LojaSerializer(loja, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(LojaSerializer(serializer.save()).data)
