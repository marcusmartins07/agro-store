from rest_framework import viewsets, permissions
from .models import Avaliacao
from .serializers import AvaliacaoSerializer


class AvaliacaoViewSet(viewsets.ModelViewSet):
    serializer_class = AvaliacaoSerializer
    http_method_names = ['get', 'post']

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        produto_id = self.request.query_params.get('produto')
        queryset = Avaliacao.objects.select_related('usuario', 'produto')
        if produto_id:
            queryset = queryset.filter(produto_id=produto_id)
        return queryset

    def perform_create(self, serializer):
        pedido_item = serializer.validated_data['pedido_item']
        serializer.save(
            usuario=self.request.user,
            produto=pedido_item.produto
        )