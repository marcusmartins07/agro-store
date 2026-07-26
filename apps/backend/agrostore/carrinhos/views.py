from rest_framework import viewsets, permissions
from .models import Carrinho
from .serializers import CarrinhoSerializer


class CarrinhoViewSet(viewsets.ModelViewSet):
    serializer_class = CarrinhoSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        # filtra somente os itens do usuário logado
        return Carrinho.objects.filter(
            usuario=self.request.user
        ).select_related('produto', 'loja')

    def perform_create(self, serializer):
        usuario = self.request.user
        produto = serializer.validated_data['produto']

        # se produto já existe no carrinho, soma a quantidade
        existente = Carrinho.objects.filter(usuario=usuario, produto=produto).first()
        if existente:
            existente.quantidade += serializer.validated_data.get('quantidade', 1)
            existente.save()
        else:
            serializer.save(usuario=usuario)