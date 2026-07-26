from django.db import models
from agrostore.main.models import BaseModel
from agrostore.usuarios.models import Usuario
from agrostore.produtos.models import Produto
from agrostore.lojas.models import Loja


class Carrinho(BaseModel):
    carrinho_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='carrinho')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('usuario', 'produto')  # mesmo produto não duplica

    def __str__(self):
        return f"{self.usuario.nome} - {self.produto.nome} x{self.quantidade}"

    @property
    def subtotal(self):
        preco = self.produto.precos.filter(vigencia_fim__isnull=True).last()
        if preco:
            return (preco.preco_desconto or preco.preco_venda) * self.quantidade
        return 0