from rest_framework import serializers

from .models import Avaliacao


class AvaliacaoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.StringRelatedField(source='produto', read_only=True)
    usuario_nome = serializers.StringRelatedField(source='usuario', read_only=True)

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

    def validate_pedido_produto(self, value):
        usuario = self.context['request'].user

        if value.pedido.usuario != usuario:
            raise serializers.ValidationError("Este item não pertence ao seu pedido.")

        if value.pedido.status.status != 'Entregue':
            raise serializers.ValidationError("Só é possível avaliar pedidos entregues.")

        if Avaliacao.objects.filter(pedido_produto=value).exists():
            raise serializers.ValidationError("Este item já foi avaliado.")

        return value
