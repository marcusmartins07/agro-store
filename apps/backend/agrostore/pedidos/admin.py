from django.contrib import admin

from .models import Pedido, PedidoCliente, PedidoProduto, StatusPedido


class SomenteConsultaMixin:
    # RN-019: pedidos ficam apenas para consulta; o status muda somente pela API.
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PedidoProdutoInline(SomenteConsultaMixin, admin.TabularInline):
    model = PedidoProduto
    extra = 0


class PedidoClienteInline(SomenteConsultaMixin, admin.StackedInline):
    model = PedidoCliente
    extra = 0
    max_num = 1
    raw_id_fields = ['usuario']


@admin.register(StatusPedido)
class StatusPedidoAdmin(admin.ModelAdmin):
    list_display = ['status_pedido_id', 'status']
    search_fields = ['status']


@admin.register(Pedido)
class PedidoAdmin(SomenteConsultaMixin, admin.ModelAdmin):
    list_display = ['pedido_id', 'cliente__usuario', 'loja', 'status', 'valor_liquido', 'data_criacao']
    list_filter = ['status', 'loja']
    list_select_related = ['loja', 'status', 'cliente__usuario']
    search_fields = ['cliente__usuario__nome', 'cliente__usuario__cpf', 'loja__nome']
    inlines = [PedidoProdutoInline, PedidoClienteInline]
