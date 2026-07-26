from rest_framework import serializers
from .models import Carrinho


class CarrinhoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.StringRelatedField(source='produto', read_only=True)
    loja_nome = serializers.StringRelatedField(source='loja', read_only=True)
    subtotal = serializers.ReadOnlyField()
    preco_unitario = serializers.SerializerMethodField()

    class Meta:
        model = Carrinho
        fields = [
            'carrinho_id',
            'produto',
            'produto_nome',
            'loja',
            'loja_nome',
            'preco_unitario',
            'quantidade',
            'subtotal',
        ]
        read_only_fields = ['usuario']

    def get_preco_unitario(self, obj):
        preco = obj.produto.precos.filter(vigencia_fim__isnull=True).last()
        if preco:
            return preco.preco_desconto or preco.preco_venda
        return None