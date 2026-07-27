from rest_framework import serializers

from agrostore.produtos.models import Produto
from .models import Carrinho, CarrinhoProduto


class CarrinhoProdutoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.StringRelatedField(source='produto', read_only=True)
    loja = serializers.IntegerField(source='carrinho.loja_id', read_only=True)
    loja_nome = serializers.StringRelatedField(source='carrinho.loja', read_only=True)
    valor_unitario = serializers.ReadOnlyField()
    valor_desconto = serializers.ReadOnlyField()
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = CarrinhoProduto
        fields = [
            'carrinho_produto_id',
            'carrinho',
            'produto',
            'produto_nome',
            'loja',
            'loja_nome',
            'valor_unitario',
            'valor_desconto',
            'quantidade',
            'subtotal',
        ]
        read_only_fields = ['carrinho']


class CarrinhoSerializer(serializers.ModelSerializer):
    loja_nome = serializers.StringRelatedField(source='loja', read_only=True)
    itens = CarrinhoProdutoSerializer(many=True, read_only=True)

    class Meta:
        model = Carrinho
        fields = [
            'carrinho_id',
            'loja',
            'loja_nome',
            'valor_bruto',
            'valor_desconto',
            'valor_liquido',
            'itens',
        ]
        read_only_fields = ['valor_bruto', 'valor_desconto', 'valor_liquido']


class AdicionarCarrinhoProdutoSerializer(serializers.Serializer):
    produto = serializers.PrimaryKeyRelatedField(queryset=Produto.objects.select_related('loja').all())
    quantidade = serializers.IntegerField(min_value=1, default=1)

    def validate_produto(self, produto):
        if not produto.ativo:
            raise serializers.ValidationError("Produto inativo não pode ser adicionado ao carrinho.")
        if not produto.loja.ativa:
            raise serializers.ValidationError("Produto de loja inativa não pode ser adicionado ao carrinho.")
        return produto


class AtualizarCarrinhoProdutoSerializer(serializers.Serializer):
    quantidade = serializers.IntegerField(min_value=1)
