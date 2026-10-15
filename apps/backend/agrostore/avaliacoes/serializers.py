from rest_framework import serializers

from agrostore.pedidos.models import Pedido, PedidoProduto
from .models import Avaliacao


def abreviar_nome(nome):
    partes = (nome or '').split()
    if len(partes) < 2:
        return ' '.join(partes)
    return f"{partes[0]} {partes[-1][0]}."


class AvaliacaoSerializer(serializers.ModelSerializer):
    # Declarado sem o UniqueValidator automático do OneToOne para validar a autoria antes da duplicidade.
    pedido_produto = serializers.PrimaryKeyRelatedField(
        queryset=PedidoProduto.objects.all(),
        error_messages={'does_not_exist': 'Este item não pertence ao seu pedido.'},
    )
    produto_nome = serializers.StringRelatedField(source='produto', read_only=True)
    usuario_nome = serializers.SerializerMethodField()
    comentario = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True,
        error_messages={'max_length': 'O comentário deve ter no máximo 500 caracteres.'},
    )

    class Meta:
        model = Avaliacao
        fields = [
            'avaliacao_id',
            'pedido_produto',
            'produto',
            'produto_nome',
            'usuario_nome',
            'nota',
            'comentario',
        ]
        read_only_fields = ['usuario', 'produto']

    def get_usuario_nome(self, avaliacao):
        return abreviar_nome(avaliacao.usuario.nome)

    def validate_pedido_produto(self, value):
        usuario = self.context['request'].user
        pedido = Pedido.objects.select_related('status').filter(pk=value.pedido_id, cliente__usuario=usuario).first()

        if pedido is None:
            raise serializers.ValidationError("Este item não pertence ao seu pedido.")

        if pedido.status.status != 'Entregue':
            raise serializers.ValidationError("Só é possível avaliar pedidos entregues.")

        if Avaliacao.objects.filter(pedido_produto=value).exists():
            raise serializers.ValidationError("Este item já foi avaliado.")

        return value
