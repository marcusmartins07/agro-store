from django.db import models
from agrostore.main.models import BaseModel
from agrostore.usuarios.models import Usuario
from agrostore.produtos.models import Produto
from agrostore.lojas.models import Loja


class Pedido(BaseModel):

    class Status(models.TextChoices):
        PENDENTE = 'P', 'Pendente'
        EM_PREPARO = 'EP', 'Em Preparo'
        PRONTO = 'PR', 'Pronto para Entrega'
        ENTREGUE = 'E', 'Entregue'
        CANCELADO = 'C', 'Cancelado'

    pedido_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pedidos')
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, related_name='pedidos')  # ← cada pedido pertence a uma loja
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PENDENTE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_com_desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido #{self.pedido_id} - {self.loja.nome}"


class PedidoItem(BaseModel):
    pedido_item_id = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome_produto = models.CharField(max_length=155)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    preco_desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade}x {self.nome_produto}"


class PedidoCliente(BaseModel):
    pedido_cliente_id = models.AutoField(primary_key=True)
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='cliente')
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11)
    email = models.EmailField()
    data_nascimento = models.DateField()
    genero = models.CharField(max_length=1)

    def __str__(self):
        return f"Cliente {self.nome} - Pedido #{self.pedido.pedido_id}"