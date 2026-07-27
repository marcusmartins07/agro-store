from rest_framework import serializers

from .models import Pedido, PedidoCliente, PedidoProduto, StatusPedido


class StatusPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusPedido
        fields = [
            'status_pedido_id',
            'status',
        ]


class PedidoProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoProduto
        fields = [
            'pedido_produto_id',
            'produto',
            'nome_produto',
            'quantidade',
            'valor_unitario',
            'valor_desconto',
            'subtotal',
        ]
        read_only_fields = ['nome_produto', 'valor_unitario', 'valor_desconto', 'subtotal']


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
    itens = PedidoProdutoSerializer(many=True, read_only=True)
    cliente = PedidoClienteSerializer(read_only=True)
    status_nome = serializers.StringRelatedField(source='status', read_only=True)
    loja_nome = serializers.StringRelatedField(source='loja', read_only=True)

    class Meta:
        model = Pedido
        fields = [
            'pedido_id',
            'loja',
            'loja_nome',
            'status',
            'status_nome',
            'valor_bruto',
            'valor_desconto',
            'valor_liquido',
            'itens',
            'cliente',
        ]
        read_only_fields = ['valor_bruto', 'valor_desconto', 'valor_liquido']


class CriarPedidoSerializer(serializers.Serializer):
    carrinho_produto_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        help_text="Lista de IDs dos itens do carrinho para gerar o pedido",
    )
