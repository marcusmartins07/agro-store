from rest_framework import serializers

from agrostore.produtos.serializers import ProdutoSerializer

from .models import Favorito


class ProdutoFavoritoSerializer(ProdutoSerializer):
    disponivel = serializers.BooleanField(source='disponivel_para_compra', read_only=True)

    class Meta(ProdutoSerializer.Meta):
        fields = ProdutoSerializer.Meta.fields + ['disponivel']


class FavoritoSerializer(serializers.ModelSerializer):
    dados_produto = ProdutoFavoritoSerializer(source='produto', read_only=True)

    class Meta:
        model = Favorito
        fields = [
            'favorito_id',
            'produto',
            'dados_produto',
            'data_criacao',
        ]
        read_only_fields = ['usuario', 'data_criacao']
