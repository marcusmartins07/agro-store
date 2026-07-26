from rest_framework import serializers
from .models import Favorito


class FavoritoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.StringRelatedField(source='produto', read_only=True)
    loja_nome = serializers.StringRelatedField(source='produto.loja', read_only=True)
    preco = serializers.SerializerMethodField()

    class Meta:
        model = Favorito
        fields = [
            'favorito_id',
            'produto',
            'produto_nome',
            'loja_nome',
            'preco',
        ]
        read_only_fields = ['usuario']

    def get_preco(self, obj):
        preco = obj.produto.precos.filter(vigencia_fim__isnull=True).last()
        if preco:
            return preco.preco_desconto or preco.preco_venda
        return None