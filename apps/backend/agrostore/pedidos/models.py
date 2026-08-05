from django.db import models

from agrostore.lojas.models import Loja
from agrostore.main.models import BaseModel
from agrostore.produtos.models import Produto
from agrostore.usuarios.models import Usuario


class StatusPedido(models.Model):
    status_pedido_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=55, unique=True)

    class Meta:
        verbose_name = 'status do pedido'
        verbose_name_plural = 'status dos pedidos'

    def __str__(self):
        return self.status


class Pedido(BaseModel):
    pedido_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pedidos')
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, related_name='pedidos')
    status = models.ForeignKey(StatusPedido, on_delete=models.PROTECT, related_name='pedidos')
    valor_bruto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_liquido = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido #{self.pedido_id} - {self.loja.nome}"


class PedidoProduto(BaseModel):
    pedido_produto_id = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome_produto = models.CharField(max_length=155)
    quantidade = models.PositiveIntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade}x {self.nome_produto}"


class PedidoCliente(BaseModel):
    pedido_cliente_id = models.AutoField(primary_key=True)
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='cliente')
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11)
    email = models.EmailField()
    telefone = models.CharField(max_length=11, null=True, blank=True)
    data_nascimento = models.DateField()
    genero = models.CharField(max_length=55)

    def __str__(self):
        return f"Cliente {self.nome} - Pedido #{self.pedido.pedido_id}"
