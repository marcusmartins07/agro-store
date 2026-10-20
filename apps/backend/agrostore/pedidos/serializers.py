from rest_framework import serializers

from agrostore.avaliacoes.models import Avaliacao
from agrostore.usuarios.models import Telefone
from .models import Pedido, PedidoCliente, PedidoProduto, StatusPedido


STATUS_COM_TELEFONE = {'Pendente', 'Em preparo', 'Pronto para retirada'}


class StatusPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusPedido
        fields = [
            'status_pedido_id',
            'status',
        ]


class AvaliacaoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = ['avaliacao_id', 'nota', 'comentario']


class PedidoProdutoSerializer(serializers.ModelSerializer):
    avaliacao = AvaliacaoItemSerializer(read_only=True)

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
            'avaliacao',
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


class PedidoClienteProdutorSerializer(serializers.ModelSerializer):
    telefone = serializers.SerializerMethodField()

    class Meta:
        model = PedidoCliente
        fields = ['nome', 'telefone']

    def get_telefone(self, obj):
        if obj.pedido.status.status not in STATUS_COM_TELEFONE:
            return None
        if PedidoCliente.usuario.is_cached(obj) and hasattr(obj.usuario, 'telefone_principal_lista'):
            principais = obj.usuario.telefone_principal_lista
            return principais[0].numero if principais else None
        return Telefone.objects.filter(usuario_id=obj.usuario_id, e_principal=True).values_list('numero', flat=True).first()


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
            'data_criacao',
            'itens',
            'cliente',
        ]
        read_only_fields = ['valor_bruto', 'valor_desconto', 'valor_liquido', 'data_criacao']


class PedidoProdutorSerializer(PedidoSerializer):
    cliente = PedidoClienteProdutorSerializer(read_only=True)


class CriarPedidoSerializer(serializers.Serializer):
    carrinho_produto_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        help_text="Lista de IDs dos itens do carrinho para gerar o pedido",
    )
