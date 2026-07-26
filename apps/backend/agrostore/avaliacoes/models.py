from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from agrostore.main.models import BaseModel
from agrostore.usuarios.models import Usuario
from agrostore.produtos.models import Produto
from agrostore.pedidos.models import PedidoItem


class Avaliacao(BaseModel):
    avaliacao_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='avaliacoes')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='avaliacoes')
    pedido_item = models.OneToOneField(PedidoItem, on_delete=models.CASCADE, related_name='avaliacao')  
    nota = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(blank=True)

    def __str__(self):
        return f"{self.usuario.nome} - {self.produto.nome} ({self.nota}★)"