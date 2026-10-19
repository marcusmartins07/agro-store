import uuid
from decimal import Decimal
from pathlib import Path

from django.core.validators import FileExtensionValidator
from django.db import models, transaction
from django.utils import timezone

from agrostore.main.models import BaseModel
from agrostore.lojas.models import Loja


EXTENSOES_IMAGEM_PRODUTO = ['jpg', 'jpeg', 'png', 'webp']


def caminho_imagem_produto(produto, nome_arquivo):
    # Nome aleatório evita colisões e não expõe o nome original do arquivo enviado.
    extensao = Path(nome_arquivo).suffix.lower()
    return f'produtos/{uuid.uuid4().hex}{extensao}'


class Categoria(BaseModel):
    categoria_id = models.BigAutoField(primary_key=True, db_column='id_categoria')
    nome = models.CharField(max_length=100, unique=True)
    ativo = models.BooleanField(default=True, db_column='esta_ativa')

    class Meta:
        db_table = 'categoria'

    def __str__(self):
        return self.nome


class Produto(BaseModel):
    LIMITE_ESTOQUE_BAIXO = 5

    produto_id = models.BigAutoField(primary_key=True, default=None, db_column='id_produto')
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, related_name='produtos', db_column='id_loja')
    nome = models.CharField(max_length=155)
    descricao = models.TextField(blank=True)
    codigo_barras = models.CharField(max_length=13, blank=True)
    estoque = models.IntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    ativo = models.BooleanField(default=True, db_column='esta_ativo')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, db_column='id_categoria')

    class Meta:
        db_table = 'produto'

    def __str__(self):
        return self.nome

    @property
    def estoque_baixo(self):
        return 0 < self.estoque <= self.LIMITE_ESTOQUE_BAIXO

    @property
    def disponivel_para_compra(self):
        return self.ativo and self.loja.ativa and self.estoque > 0

    def gerar_sku(self):
        componentes = (
            ('loja', self.loja_id, 4),
            ('categoria', self.categoria_id, 4),
            ('produto', self.produto_id, 6),
        )

        for nome, valor, tamanho in componentes:
            if valor is None or valor > (10 ** tamanho) - 1:
                raise ValueError(f'Identificador de {nome} excede o limite de {tamanho} dígitos para o SKU.')

        return ''.join(f'{valor:0{tamanho}d}' for _, valor, tamanho in componentes)

    def save(self, *args, **kwargs):
        if not self._state.adding:
            return super().save(*args, **kwargs)

        self.sku = None
        with transaction.atomic():
            super().save(*args, **kwargs)
            self.sku = self.gerar_sku()
            super().save(update_fields=['sku'])


class ImagemProduto(BaseModel):
    LIMITE_POR_PRODUTO = 5

    id = models.BigAutoField(primary_key=True, db_column='id_imagem')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='imagens', db_column='id_produto')
    imagem = models.FileField(
        upload_to=caminho_imagem_produto,
        max_length=255,
        validators=[FileExtensionValidator(EXTENSOES_IMAGEM_PRODUTO)],
        db_column='caminho',
    )
    ordem = models.PositiveIntegerField(default=0)
    e_principal = models.BooleanField(default=False)

    class Meta:
        db_table = 'imagem'
        ordering = ['ordem', 'id']
        constraints = [
            models.UniqueConstraint(
                fields=['produto'],
                condition=models.Q(e_principal=True),
                name='imagem_principal_unica_por_produto',
            ),
        ]

    def __str__(self):
        return f'{self.produto.nome} - imagem {self.ordem + 1}'

    def definir_como_principal(self):
        with transaction.atomic():
            ImagemProduto.objects.filter(produto_id=self.produto_id, e_principal=True).exclude(pk=self.pk).update(e_principal=False)
            self.e_principal = True
            self.save(update_fields=['e_principal', 'data_atualizacao'])

    def excluir(self):
        # A próxima imagem pela ordem assume como principal; o arquivo só sai do storage depois da exclusão no banco.
        nome_arquivo = self.imagem.name
        storage = self.imagem.storage
        with transaction.atomic():
            era_principal = self.e_principal
            self.delete()
            if era_principal:
                proxima = ImagemProduto.objects.filter(produto_id=self.produto_id).first()
                if proxima:
                    proxima.definir_como_principal()
        storage.delete(nome_arquivo)


class PrecoProduto(BaseModel):
    id = models.BigAutoField(primary_key=True, db_column='id_preco_produto')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='precos', db_column='id_produto')
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, db_column='valor_venda')
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='valor_custo')
    preco_desconto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='valor_desconto')
    porcentagem_desconto = models.IntegerField(null=True, blank=True)
    vigencia_inicio = models.DateTimeField(default=timezone.now)
    vigencia_fim = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'preco_produto'

    def save(self, *args, **kwargs):
        if not self.pk:
            PrecoProduto.objects.filter(
                produto=self.produto,
                vigencia_fim__isnull=True
            ).update(vigencia_fim=timezone.now())

        if self.preco_venda and self.preco_desconto:
            self.porcentagem_desconto = int(
                (self.preco_desconto / self.preco_venda) * 100
            )
        elif self.preco_venda and self.porcentagem_desconto is not None:
            if 0 <= self.porcentagem_desconto <= 100:
                desconto_percentual = Decimal(self.porcentagem_desconto) / Decimal(100)
                self.preco_desconto = self.preco_venda * desconto_percentual
            else:
                raise ValueError("Porcentagem de desconto deve estar entre 0 e 100")
        else:
            self.porcentagem_desconto = None
            self.preco_desconto = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produto.nome} - R$ {self.preco_venda}"
