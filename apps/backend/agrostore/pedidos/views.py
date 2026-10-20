from collections import defaultdict
from decimal import Decimal

from django.db import transaction
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response

from agrostore.carrinhos.models import CarrinhoProduto
from agrostore.carrinhos.services import ajustar_carrinhos_ao_estoque
from agrostore.produtos.models import Produto
from agrostore.usuarios.models import Telefone
from .models import Pedido, PedidoCliente, PedidoProduto, StatusPedido
from .serializers import CriarPedidoSerializer, PedidoProdutorSerializer, PedidoSerializer, StatusPedidoSerializer


STATUS_TRANSICOES = {
    'Pendente': {'Em preparo', 'Cancelado'},
    'Em preparo': {'Pronto para retirada', 'Cancelado'},
    'Pronto para retirada': {'Entregue'},
    'Entregue': set(),
    'Cancelado': set(),
}


def garantir_status_pedidos():
    return {
        nome: StatusPedido.objects.get_or_create(status=nome)[0]
        for nome in STATUS_TRANSICOES
    }


class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch']

    def get_queryset(self):
        queryset = Pedido.objects.select_related('loja', 'status', 'cliente').prefetch_related('itens__avaliacao')
        if self.action == 'minha_loja':
            queryset = queryset.select_related('cliente__usuario').prefetch_related(
                Prefetch(
                    'cliente__usuario__telefones',
                    queryset=Telefone.objects.filter(e_principal=True),
                    to_attr='telefone_principal_lista',
                )
            )
        if self.action in ['minha_loja', 'atualizar_status']:
            if self.request.user.is_staff:
                return queryset
            return queryset.filter(loja__proprietario=self.request.user)
        return queryset.filter(cliente__usuario=self.request.user)

    @transaction.atomic
    def create(self, request):
        serializer = CriarPedidoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        carrinho_produto_ids = serializer.validated_data['carrinho_produto_ids']
        usuario = request.user
        itens_carrinho = CarrinhoProduto.objects.filter(
            carrinho_produto_id__in=carrinho_produto_ids,
            carrinho__usuario=usuario,
        ).select_related('carrinho', 'carrinho__loja')
        itens = list(itens_carrinho)

        if len(itens) != len(set(carrinho_produto_ids)):
            return Response(
                {"detail": "Um ou mais itens do carrinho são inválidos."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        produtos_travados = {
            produto.pk: produto
            for produto in Produto.objects.select_for_update().filter(pk__in={item.produto_id for item in itens}).order_by('pk')
        }
        for item in itens:
            item.produto = produtos_travados[item.produto_id]

        itens_por_loja = defaultdict(list)
        for item in itens:
            erro = self._validar_item_checkout(item)
            if erro:
                return Response({"detail": erro}, status=status.HTTP_400_BAD_REQUEST)
            itens_por_loja[item.carrinho.loja].append(item)

        status_pendente = garantir_status_pedidos()['Pendente']
        pedidos_criados = []

        for loja, itens_da_loja in itens_por_loja.items():
            valor_bruto, valor_desconto = self._calcular_totais(itens_da_loja)
            pedido = Pedido.objects.create(
                loja=loja,
                status=status_pendente,
                valor_bruto=valor_bruto,
                valor_desconto=valor_desconto,
                valor_liquido=valor_bruto - valor_desconto,
            )
            PedidoCliente.objects.create(
                pedido=pedido,
                usuario=usuario,
                nome=usuario.nome,
                cpf=usuario.cpf,
                email=usuario.email,
                data_nascimento=usuario.data_nascimento,
                genero=str(usuario.genero),
            )

            for item in itens_da_loja:
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

            pedidos_criados.append(pedido)

        carrinhos_afetados = {item.carrinho for item in itens}
        itens_carrinho.delete()
        for carrinho in carrinhos_afetados:
            if carrinho.itens.exists():
                carrinho.recalcular_totais()
            else:
                carrinho.delete()

        for produto in produtos_travados.values():
            ajustar_carrinhos_ao_estoque(produto)

        return Response(PedidoSerializer(pedidos_criados, many=True).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='status')
    @transaction.atomic
    def atualizar_status(self, request, pk=None):
        if not request.user.is_produtor and not request.user.is_staff:
            raise PermissionDenied('Somente produtores podem atualizar o status de pedidos.')
        pedido = self._obter_pedido_para_atualizacao(pk)
        status_id = request.data.get('status')
        status_pedido = StatusPedido.objects.filter(status_pedido_id=status_id).first()

        if not status_pedido:
            return Response({"detail": "Status inválido."}, status=status.HTTP_400_BAD_REQUEST)

        status_atual = pedido.status.status
        if status_pedido.status not in STATUS_TRANSICOES.get(status_atual, set()):
            return Response(
                {"detail": f"Não é possível alterar um pedido de {status_atual} para {status_pedido.status}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self._atualizar_status_pedido(pedido, status_pedido)
        return Response(PedidoProdutorSerializer(pedido).data)

    @action(detail=True, methods=['patch'], url_path='cancelar')
    @transaction.atomic
    def cancelar(self, request, pk=None):
        pedido = self._obter_pedido_para_atualizacao(pk, usuario=request.user)
        status_cancelado = garantir_status_pedidos()['Cancelado']

        if pedido.status.status != 'Pendente':
            return Response(
                {'detail': 'Somente pedidos pendentes podem ser cancelados pelo cliente.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self._atualizar_status_pedido(pedido, status_cancelado)
        return Response(PedidoSerializer(pedido).data)

    @action(detail=True, methods=['patch'], url_path='confirmar-entrega')
    @transaction.atomic
    def confirmar_entrega(self, request, pk=None):
        pedido = self._obter_pedido_para_atualizacao(pk, usuario=request.user)

        if pedido.status.status != 'Pronto para retirada':
            return Response(
                {'detail': 'Somente pedidos prontos para retirada podem ter o recebimento confirmado.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self._atualizar_status_pedido(pedido, garantir_status_pedidos()['Entregue'])
        return Response(PedidoSerializer(pedido).data)

    @action(detail=False, methods=['get'], url_path='minha-loja')
    def minha_loja(self, request):
        if not request.user.is_produtor and not request.user.is_staff:
            raise PermissionDenied('Somente produtores podem consultar pedidos da loja.')
        serializer = PedidoProdutorSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='status-disponiveis')
    def status_disponiveis(self, request):
        if not request.user.is_produtor and not request.user.is_staff:
            raise PermissionDenied('Somente produtores podem consultar os status de pedidos.')
        return Response(StatusPedidoSerializer(garantir_status_pedidos().values(), many=True).data)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PATCH', detail='Use o endpoint de status para atualizar pedidos.')

    def _validar_item_checkout(self, item):
        if item.produto.loja_id != item.carrinho.loja_id:
            return f"O produto {item.produto.nome} não pertence à loja do carrinho."
        if not item.produto.ativo:
            return f"O produto {item.produto.nome} está inativo."
        if not item.carrinho.loja.ativa:
            return f"A loja {item.carrinho.loja.nome} está inativa."
        if item.quantidade < 1:
            return f"O produto {item.produto.nome} está sem estoque. Remova-o da seleção para finalizar."
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

    def _obter_pedido_para_atualizacao(self, pedido_id, usuario=None):
        queryset = Pedido.objects.select_for_update().prefetch_related('itens__avaliacao')
        if usuario is not None:
            queryset = queryset.filter(cliente__usuario=usuario)
        elif not self.request.user.is_staff:
            queryset = queryset.filter(loja__proprietario=self.request.user)
        return get_object_or_404(queryset, pedido_id=pedido_id)

    def _atualizar_status_pedido(self, pedido, status_cancelado):
        if status_cancelado.status == 'Cancelado':
            for item in pedido.itens.all():
                if item.produto_id is None:
                    continue
                produto = Produto.objects.select_for_update().filter(produto_id=item.produto_id).first()
                if produto is None:
                    continue
                produto.estoque += item.quantidade
                produto.save(update_fields=['estoque', 'data_atualizacao'])

        pedido.status = status_cancelado
        pedido.save(update_fields=['status', 'data_atualizacao'])
