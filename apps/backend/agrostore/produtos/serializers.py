from rest_framework import serializers
from .models import Produto, PrecoProduto, Categoria, ImagemProduto


TAMANHO_MAXIMO_IMAGEM_PRODUTO = 5 * 1024 * 1024
ASSINATURAS_IMAGEM = (
    b'\xff\xd8\xff',  # JPEG
    b'\x89PNG\r\n\x1a\n',  # PNG
)


def arquivo_e_imagem(arquivo):
    arquivo.seek(0)
    cabecalho = arquivo.read(12)
    arquivo.seek(0)
    e_webp = cabecalho[:4] == b'RIFF' and cabecalho[8:12] == b'WEBP'
    return e_webp or cabecalho.startswith(ASSINATURAS_IMAGEM)


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


    def validate_porcentagem_desconto(self, valor):
        if valor is not None and not 0 <= valor <= 100:
            raise serializers.ValidationError('Informe um desconto entre 0 e 100%.')
        return valor


class ImagemProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagemProduto
        fields = ['id', 'imagem', 'ordem', 'e_principal']
        read_only_fields = ['ordem']

    def validate_imagem(self, imagem):
        if self.instance is not None:
            raise serializers.ValidationError('Para trocar a imagem, exclua esta e envie uma nova.')
        if imagem.size > TAMANHO_MAXIMO_IMAGEM_PRODUTO:
            raise serializers.ValidationError('A imagem deve ter no máximo 5 MB.')
        if not arquivo_e_imagem(imagem):
            raise serializers.ValidationError('Envie uma imagem JPG, PNG ou WEBP válida.')
        return imagem

    def validate_e_principal(self, e_principal):
        if self.instance is not None and self.instance.e_principal and not e_principal:
            raise serializers.ValidationError('Defina outra imagem como principal para desmarcar esta.')
        return e_principal


class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.StringRelatedField(source='categoria', read_only=True)
    loja_nome = serializers.StringRelatedField(source='loja', read_only=True)  # ← novo
    preco = serializers.SerializerMethodField()
    preco_original = serializers.SerializerMethodField()
    desconto = serializers.SerializerMethodField()
    imagem = serializers.SerializerMethodField()
    imagens = ImagemProdutoSerializer(many=True, read_only=True)
    estoque_baixo = serializers.ReadOnlyField()

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
            'estoque_baixo',  # leitura: estoque de 1 a Produto.LIMITE_ESTOQUE_BAIXO
            'sku',
            'ativo',
            'preco',
            'preco_original',
            'desconto',
            'imagem',         # leitura: URL da imagem principal
            'imagens',        # leitura: gerenciadas em /produtos/{id}/imagens/
        ]
        read_only_fields = ['loja', 'sku']

    def get_imagem(self, obj):
        principal = next((imagem for imagem in obj.imagens.all() if imagem.e_principal), None)
        if principal is None:
            return None
        url = principal.imagem.url
        request = self.context.get('request')
        return request.build_absolute_uri(url) if request else url

    def validate_estoque(self, estoque):
        if estoque < 0:
            raise serializers.ValidationError('O estoque não pode ser negativo.')
        return estoque

    def validate(self, attrs):
        categoria = attrs.get('categoria')
        if categoria is not None and not categoria.ativo:
            raise serializers.ValidationError({
                'categoria': 'A categoria selecionada está inativa e não pode ser usada em novos cadastros ou alterações.'
            })
        return attrs

    def get_preco_atual(self, obj):
        return obj.precos.filter(vigencia_fim__isnull=True).last()

    def get_preco(self, obj):
        preco = self.get_preco_atual(obj)
        if preco:
            return preco.preco_venda - (preco.preco_desconto or 0)
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
