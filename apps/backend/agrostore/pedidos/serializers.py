from rest_framework import serializers
from .models import Pedido, PedidoItem, PedidoCliente


class PedidoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoItem
        fields = [
            'pedido_item_id',
            'produto',
            'nome_produto',
            'quantidade',
            'preco_unitario',
            'preco_desconto',
            'subtotal',
        ]
        read_only_fields = ['nome_produto', 'preco_unitario', 'preco_desconto', 'subtotal']


class PedidoClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoCliente
        fields = [
            'pedido_cliente_id',
            'nome',
            'cpf',
            'email',
            'data_nascimento',
            'genero',
        ]


class PedidoSerializer(serializers.ModelSerializer):
    itens = PedidoItemSerializer(many=True, read_only=True)
    cliente = PedidoClienteSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    loja_nome = serializers.StringRelatedField(source='loja', read_only=True)

    class Meta:
        model = Pedido
        fields = [
            'pedido_id',
            'loja',
            'loja_nome',
            'status',
            'status_display',
            'total',
            'total_desconto',
            'total_com_desconto',
            'itens',
            'cliente',
        ]
        read_only_fields = ['total', 'total_desconto', 'total_com_desconto']


class CriarPedidoSerializer(serializers.Serializer):
    carrinho_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="Lista de IDs do carrinho para gerar o pedido"
    )