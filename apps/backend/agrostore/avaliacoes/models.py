from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from agrostore.main.models import BaseModel
from agrostore.usuarios.models import Usuario
from agrostore.produtos.models import Produto
from agrostore.pedidos.models import PedidoProduto


class Avaliacao(BaseModel):
    avaliacao_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='avaliacoes')
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True, blank=True, related_name='avaliacoes')
    pedido_produto = models.OneToOneField(PedidoProduto, on_delete=models.CASCADE, related_name='avaliacao')
    nota = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(blank=True)

    def __str__(self):
        nome_produto = self.produto.nome if self.produto_id else self.pedido_produto.nome_produto
        return f"{self.usuario.nome} - {nome_produto} ({self.nota}★)"
