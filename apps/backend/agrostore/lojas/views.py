from rest_framework import viewsets, permissions
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