from django.db import models
from decimal import Decimal
from django.utils import timezone
from agrostore.main.models import BaseModel
from agrostore.lojas.models import Loja


class Categoria(BaseModel):
    categoria_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Produto(BaseModel):
    produto_id = models.AutoField(primary_key=True, default=None)
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, related_name='produtos')
    nome = models.CharField(max_length=155)
    descricao = models.TextField(blank=True)
    codigo_barras = models.CharField(max_length=13, blank=True)
    estoque = models.IntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True, blank=True)
    ativo = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome


class PrecoProduto(BaseModel):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='precos')
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    preco_desconto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    porcentagem_desconto = models.IntegerField(null=True, blank=True)
    vigencia_inicio = models.DateTimeField(default=timezone.now)
    vigencia_fim = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            PrecoProduto.objects.filter(
                produto=self.produto,
                vigencia_fim__isnull=True
            ).update(vigencia_fim=timezone.now())

        if self.preco_venda and self.preco_desconto:
            self.porcentagem_desconto = int(
                ((self.preco_venda - self.preco_desconto) / self.preco_venda) * 100
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