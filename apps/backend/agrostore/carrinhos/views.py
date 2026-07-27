from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Carrinho, CarrinhoProduto
from .serializers import (
    AdicionarCarrinhoProdutoSerializer,
    AtualizarCarrinhoProdutoSerializer,
    CarrinhoProdutoSerializer,
    CarrinhoSerializer,
)


class CarrinhoViewSet(viewsets.ModelViewSet):
    serializer_class = CarrinhoSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return Carrinho.objects.filter(
            usuario=self.request.user
        ).select_related('loja').prefetch_related('itens__produto__precos')

    def get_serializer_class(self):
        if self.action == 'create':
            return AdicionarCarrinhoProdutoSerializer
        return CarrinhoSerializer

    @transaction.atomic
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        produto = serializer.validated_data['produto']
        quantidade = serializer.validated_data['quantidade']
        item = CarrinhoProduto.objects.filter(carrinho__usuario=request.user, produto=produto).first()
        quantidade_final = quantidade + (item.quantidade if item else 0)

        if quantidade_final > produto.estoque:
            return Response(
                {"detail": "Produto sem estoque suficiente para a quantidade solicitada."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if item:
            carrinho = item.carrinho
            item.quantidade = quantidade_final
            item.save(update_fields=['quantidade', 'data_atualizacao'])
        else:
            carrinho, _ = Carrinho.objects.get_or_create(usuario=request.user, loja=produto.loja)
            item = CarrinhoProduto.objects.create(carrinho=carrinho, produto=produto, quantidade=quantidade)

        carrinho.recalcular_totais()
        return Response(CarrinhoProdutoSerializer(item).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['patch'], url_path=r'itens/(?P<item_id>[^/.]+)')
    @transaction.atomic
    def atualizar_item(self, request, item_id=None):
        item = self._get_item_do_usuario(request, item_id)
        serializer = AtualizarCarrinhoProdutoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quantidade = serializer.validated_data['quantidade']
        if quantidade > item.produto.estoque:
            return Response(
                {"detail": "Produto sem estoque suficiente para a quantidade solicitada."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        item.quantidade = quantidade
        item.save(update_fields=['quantidade', 'data_atualizacao'])
        item.carrinho.recalcular_totais()
        return Response(CarrinhoProdutoSerializer(item).data)

    @action(detail=False, methods=['delete'], url_path=r'itens/(?P<item_id>[^/.]+)')
    @transaction.atomic
    def remover_item(self, request, item_id=None):
        item = self._get_item_do_usuario(request, item_id)
        carrinho = item.carrinho
        item.delete()

        if carrinho.itens.exists():
            carrinho.recalcular_totais()
        else:
            carrinho.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def _get_item_do_usuario(self, request, item_id):
        return get_object_or_404(CarrinhoProduto.objects.select_related(
            'carrinho',
            'produto',
        ), carrinho__usuario=request.user, carrinho_produto_id=item_id)
