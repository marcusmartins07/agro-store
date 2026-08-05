from rest_framework import serializers

from agrostore.produtos.serializers import ProdutoSerializer

from .models import Favorito


class ProdutoFavoritoSerializer(ProdutoSerializer):
    disponivel = serializers.SerializerMethodField()

    class Meta(ProdutoSerializer.Meta):
        fields = ProdutoSerializer.Meta.fields + ['disponivel']

    def get_disponivel(self, produto):
        return produto.ativo and produto.loja.ativa and produto.estoque > 0


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
