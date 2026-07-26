from rest_framework import serializers
from .models import Produto, PrecoProduto, Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = (
            'categoria_id',
            'nome',
            'ativo'
        )


class PrecoProdutoSerializer(serializers.ModelSerializer):
    preco_desconto = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    vigencia_inicio = serializers.DateTimeField(read_only=True)
    vigencia_fim = serializers.DateTimeField(read_only=True)

    class Meta:
        model = PrecoProduto
        fields = [
            'id',
            'produto',
            'preco_venda',
            'preco_custo',
            'preco_desconto',
            'porcentagem_desconto',
            'vigencia_inicio',
            'vigencia_fim',
        ]


class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.StringRelatedField(source='categoria', read_only=True)
    loja_nome = serializers.StringRelatedField(source='loja', read_only=True)  # ← novo
    preco = serializers.SerializerMethodField()
    preco_original = serializers.SerializerMethodField()
    desconto = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = [
            'produto_id',
            'loja',           # escrita
            'loja_nome',      # leitura
            'nome',
            'descricao',
            'categoria',      # escrita
            'categoria_nome', # leitura
            'codigo_barras',
            'estoque',
            'sku',
            'preco',
            'preco_original',
            'desconto',
        ]

    def get_preco_atual(self, obj):
        return obj.precos.filter(vigencia_fim__isnull=True).last()

    def get_preco(self, obj):
        preco = self.get_preco_atual(obj)
        if preco:
            return preco.preco_desconto or preco.preco_venda
        return None

    def get_preco_original(self, obj):
        preco = self.get_preco_atual(obj)
        if preco:
            return preco.preco_venda
        return None

    def get_desconto(self, obj):
        preco = self.get_preco_atual(obj)
        if preco:
            return preco.porcentagem_desconto
        return None