from django.db import models

from agrostore.lojas.models import Loja
from agrostore.main.models import BaseModel
from agrostore.produtos.models import Produto
from agrostore.usuarios.models import Usuario


class StatusPedido(models.Model):
    status_pedido_id = models.BigAutoField(primary_key=True, db_column='id_status_pedido')
    status = models.CharField(max_length=55, unique=True, db_column='nome')

    class Meta:
        db_table = 'status_pedido'
        verbose_name = 'status do pedido'
        verbose_name_plural = 'status dos pedidos'

    def __str__(self):
        return self.status


class Pedido(BaseModel):
    pedido_id = models.BigAutoField(primary_key=True, db_column='id_pedido')
    loja = models.ForeignKey(Loja, on_delete=models.PROTECT, related_name='pedidos', db_column='id_loja')
    status = models.ForeignKey(StatusPedido, on_delete=models.PROTECT, related_name='pedidos', db_column='id_status_pedido')
    valor_bruto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_liquido = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = 'pedido'

    def __str__(self):
        return f"Pedido #{self.pedido_id} - {self.loja.nome}"


class PedidoProduto(BaseModel):
    pedido_produto_id = models.BigAutoField(primary_key=True, db_column='id_pedido_produto')
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens', db_column='id_pedido')
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_produto')
    nome_produto = models.CharField(max_length=155)
    quantidade = models.PositiveIntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'pedido_produto'
        constraints = [
            models.CheckConstraint(condition=models.Q(quantidade__gt=0), name='pedido_produto_quantidade_positiva'),
            models.CheckConstraint(condition=models.Q(valor_unitario__gte=0), name='pedido_produto_valor_unitario_nao_negativo'),
            models.CheckConstraint(condition=models.Q(valor_desconto__gte=0), name='pedido_produto_valor_desconto_nao_negativo'),
            models.CheckConstraint(condition=models.Q(subtotal__gte=0), name='pedido_produto_subtotal_nao_negativo'),
        ]

    def __str__(self):
        return f"{self.quantidade}x {self.nome_produto}"


class PedidoCliente(BaseModel):
    pedido_cliente_id = models.BigAutoField(primary_key=True, db_column='id_pedido_cliente')
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='cliente', db_column='id_pedido')
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='pedidos_cliente', db_column='id_usuario')
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11)
    email = models.EmailField()
    data_nascimento = models.DateField()
    genero = models.CharField(max_length=55)

    class Meta:
        db_table = 'pedido_cliente'

    def __str__(self):
        return f"Cliente {self.nome} - Pedido #{self.pedido.pedido_id}"
