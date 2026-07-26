from rest_framework import serializers
from agrostore.pedidos.models import PedidoItem, Pedido
from .models import Avaliacao


class AvaliacaoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.StringRelatedField(source='produto', read_only=True)
    usuario_nome = serializers.StringRelatedField(source='usuario', read_only=True)

    class Meta:
        model = Avaliacao
        fields = [
            'avaliacao_id',
            'pedido_item',
            'produto',
            'produto_nome',
            'usuario_nome',
            'nota',
            'comentario',
        ]
        read_only_fields = ['usuario', 'produto']

    def validate_pedido_item(self, value):
        usuario = self.context['request'].user

        # Verifica se o pedido_item pertence ao usuário logado
        if value.pedido.usuario != usuario:
            raise serializers.ValidationError("Este item não pertence ao seu pedido.")

        # Verifica se o pedido está entregue
        if value.pedido.status != Pedido.Status.ENTREGUE:
            raise serializers.ValidationError("Só é possível avaliar pedidos entregues.")

        # Verifica se já existe avaliação para este item
        if Avaliacao.objects.filter(pedido_item=value).exists():
            raise serializers.ValidationError("Este item já foi avaliado.")

        return value