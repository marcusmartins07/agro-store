from django.contrib import admin

from .models import Pedido, PedidoCliente, PedidoProduto, StatusPedido


class PedidoProdutoInline(admin.TabularInline):
    model = PedidoProduto
    extra = 0


class PedidoClienteInline(admin.StackedInline):
    model = PedidoCliente
    extra = 0
    max_num = 1


@admin.register(StatusPedido)
class StatusPedidoAdmin(admin.ModelAdmin):
    list_display = ['status_pedido_id', 'status']
    search_fields = ['status']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido_id', 'usuario', 'loja', 'status', 'valor_liquido', 'data_criacao']
    list_filter = ['status', 'loja']
    search_fields = ['usuario__nome', 'usuario__cpf', 'loja__nome']
    inlines = [PedidoProdutoInline, PedidoClienteInline]
