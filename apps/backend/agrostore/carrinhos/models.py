from decimal import Decimal

from django.db import models

from agrostore.lojas.models import Loja
from agrostore.main.models import BaseModel
from agrostore.produtos.models import Produto
from agrostore.usuarios.models import Usuario


class Carrinho(BaseModel):
    carrinho_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='carrinhos')
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
    valor_bruto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_liquido = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('usuario', 'loja')

    def __str__(self):
        return f"{self.usuario.nome} - {self.loja.nome}"

    def recalcular_totais(self):
        valor_bruto = Decimal('0.00')
        valor_desconto = Decimal('0.00')

        for item in self.itens.select_related('produto').prefetch_related('produto__precos'):
            preco = item.preco_atual
            if not preco:
                continue

            desconto_unitario = preco.preco_desconto or Decimal('0.00')
            valor_bruto += preco.preco_venda * item.quantidade
            valor_desconto += desconto_unitario * item.quantidade

        self.valor_bruto = valor_bruto
        self.valor_desconto = valor_desconto
        self.valor_liquido = valor_bruto - valor_desconto
        self.save(update_fields=['valor_bruto', 'valor_desconto', 'valor_liquido', 'data_atualizacao'])


class CarrinhoProduto(BaseModel):
    carrinho_produto_id = models.AutoField(primary_key=True)
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='itens_carrinho')
    quantidade = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('carrinho', 'produto')

    def __str__(self):
        return f"{self.produto.nome} x{self.quantidade}"

    @property
    def preco_atual(self):
        return self.produto.precos.filter(vigencia_fim__isnull=True).last()

    @property
    def valor_unitario(self):
        preco = self.preco_atual
        return preco.preco_venda if preco else None

    @property
    def valor_desconto(self):
        preco = self.preco_atual
        return preco.preco_desconto or Decimal('0.00') if preco else Decimal('0.00')

    @property
    def subtotal(self):
        if self.valor_unitario is None:
            return Decimal('0.00')
        return (self.valor_unitario - self.valor_desconto) * self.quantidade
