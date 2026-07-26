from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from collections import defaultdict
from agrostore.carrinhos.models import Carrinho
from .models import Pedido, PedidoItem, PedidoCliente
from .serializers import PedidoSerializer, CriarPedidoSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch']

    def get_queryset(self):
        return Pedido.objects.filter(
            usuario=self.request.user
        ).prefetch_related('itens', 'cliente')

    @transaction.atomic
    def create(self, request):
        serializer = CriarPedidoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        carrinho_ids = serializer.validated_data['carrinho_ids']
        usuario = request.user

        itens_carrinho = Carrinho.objects.filter(
            carrinho_id__in=carrinho_ids,
            usuario=usuario
        ).select_related('produto', 'loja')

        if not itens_carrinho.exists():
            return Response(
                {"detail": "Nenhum item válido encontrado no carrinho."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Agrupa itens por loja
        itens_por_loja = defaultdict(list)
        for item in itens_carrinho:
            itens_por_loja[item.loja].append(item)

        pedidos_criados = []

        # Cria um pedido para cada loja
        for loja, itens in itens_por_loja.items():
            total = 0
            total_desconto = 0

            for item in itens:
                preco = item.produto.precos.filter(vigencia_fim__isnull=True).last()
                preco_unitario = preco.preco_venda if preco else 0
                preco_desc = preco.preco_desconto or 0 if preco else 0
                total += preco_unitario * item.quantidade
                total_desconto += preco_desc * item.quantidade

            total_com_desconto = total - total_desconto

            pedido = Pedido.objects.create(
                usuario=usuario,
                loja=loja,
                total=total,
                total_desconto=total_desconto,
                total_com_desconto=total_com_desconto
            )

            for item in itens:
                preco = item.produto.precos.filter(vigencia_fim__isnull=True).last()
                preco_unitario = preco.preco_venda if preco else 0
                preco_desc = preco.preco_desconto or 0 if preco else 0

                PedidoItem.objects.create(
                    pedido=pedido,
                    produto=item.produto,
                    nome_produto=item.produto.nome,
                    quantidade=item.quantidade,
                    preco_unitario=preco_unitario,
                    preco_desconto=preco_desc,
                    subtotal=(preco_unitario - preco_desc) * item.quantidade
                )

            PedidoCliente.objects.create(
                pedido=pedido,
                nome=usuario.nome,
                cpf=usuario.cpf,
                email=usuario.email,
                data_nascimento=usuario.data_nascimento,
                genero=usuario.genero,
            )

            pedidos_criados.append(pedido)

        # Remove os itens do carrinho após gerar os pedidos
        itens_carrinho.delete()

        return Response(
            PedidoSerializer(pedidos_criados, many=True).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['patch'], url_path='status')
    def atualizar_status(self, request, pk=None):
        pedido = self.get_object()
        novo_status = request.data.get('status')

        if novo_status not in dict(Pedido.Status.choices):
            return Response(
                {"detail": "Status inválido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        pedido.status = novo_status
        pedido.save()
        return Response(PedidoSerializer(pedido).data)