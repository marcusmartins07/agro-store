from collections import defaultdict
from decimal import Decimal

from django.db import transaction
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from agrostore.carrinhos.models import CarrinhoProduto
from .models import Pedido, PedidoCliente, PedidoProduto, StatusPedido
from .serializers import CriarPedidoSerializer, PedidoSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch']

    def get_queryset(self):
        return Pedido.objects.filter(
            usuario=self.request.user
        ).select_related('loja', 'status').prefetch_related('itens', 'cliente')

    @transaction.atomic
    def create(self, request):
        serializer = CriarPedidoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        carrinho_produto_ids = serializer.validated_data['carrinho_produto_ids']
        usuario = request.user
        itens_carrinho = CarrinhoProduto.objects.filter(
            carrinho_produto_id__in=carrinho_produto_ids,
            carrinho__usuario=usuario,
        ).select_related('carrinho', 'carrinho__loja', 'produto')

        if itens_carrinho.count() != len(set(carrinho_produto_ids)):
            return Response(
                {"detail": "Um ou mais itens do carrinho são inválidos."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        itens_por_loja = defaultdict(list)
        for item in itens_carrinho:
            erro = self._validar_item_checkout(item)
            if erro:
                return Response({"detail": erro}, status=status.HTTP_400_BAD_REQUEST)
            itens_por_loja[item.carrinho.loja].append(item)

        status_pendente, _ = StatusPedido.objects.get_or_create(status='Pendente')
        pedidos_criados = []

        for loja, itens in itens_por_loja.items():
            valor_bruto, valor_desconto = self._calcular_totais(itens)
            pedido = Pedido.objects.create(
                usuario=usuario,
                loja=loja,
                status=status_pendente,
                valor_bruto=valor_bruto,
                valor_desconto=valor_desconto,
                valor_liquido=valor_bruto - valor_desconto,
            )

            for item in itens:
                preco = item.preco_atual
                desconto_unitario = preco.preco_desconto or Decimal('0.00')
                PedidoProduto.objects.create(
                    pedido=pedido,
                    produto=item.produto,
                    nome_produto=item.produto.nome,
                    quantidade=item.quantidade,
                    valor_unitario=preco.preco_venda,
                    valor_desconto=desconto_unitario,
                    subtotal=(preco.preco_venda - desconto_unitario) * item.quantidade,
                )

                item.produto.estoque -= item.quantidade
                item.produto.save(update_fields=['estoque', 'data_atualizacao'])

            PedidoCliente.objects.create(
                pedido=pedido,
                nome=usuario.nome,
                cpf=usuario.cpf,
                email=usuario.email,
                telefone=usuario.telefone,
                data_nascimento=usuario.data_nascimento,
                genero=str(usuario.genero),
            )
            pedidos_criados.append(pedido)

        carrinhos_afetados = {item.carrinho for item in itens_carrinho}
        itens_carrinho.delete()
        for carrinho in carrinhos_afetados:
            if carrinho.itens.exists():
                carrinho.recalcular_totais()
            else:
                carrinho.delete()

        return Response(PedidoSerializer(pedidos_criados, many=True).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='status')
    def atualizar_status(self, request, pk=None):
        pedido = self.get_object()
        status_id = request.data.get('status')
        status_pedido = StatusPedido.objects.filter(status_pedido_id=status_id).first()

        if not status_pedido:
            return Response({"detail": "Status inválido."}, status=status.HTTP_400_BAD_REQUEST)

        pedido.status = status_pedido
        pedido.save(update_fields=['status', 'data_atualizacao'])
        return Response(PedidoSerializer(pedido).data)

    def _validar_item_checkout(self, item):
        if not item.produto.ativo:
            return f"O produto {item.produto.nome} está inativo."
        if not item.carrinho.loja.ativa:
            return f"A loja {item.carrinho.loja.nome} está inativa."
        if item.quantidade > item.produto.estoque:
            return f"O produto {item.produto.nome} não possui estoque suficiente."
        if not item.preco_atual:
            return f"O produto {item.produto.nome} não possui preço vigente."
        return None

    def _calcular_totais(self, itens):
        valor_bruto = Decimal('0.00')
        valor_desconto = Decimal('0.00')

        for item in itens:
            preco = item.preco_atual
            valor_bruto += preco.preco_venda * item.quantidade
            valor_desconto += (preco.preco_desconto or Decimal('0.00')) * item.quantidade

        return valor_bruto, valor_desconto
