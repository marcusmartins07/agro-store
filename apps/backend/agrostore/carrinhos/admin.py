from django.contrib import admin

from .models import Carrinho, CarrinhoProduto


class CarrinhoProdutoInline(admin.TabularInline):
    model = CarrinhoProduto
    extra = 0


@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ['carrinho_id', 'usuario', 'loja', 'valor_liquido', 'data_atualizacao']
    list_filter = ['loja']
    search_fields = ['usuario__nome', 'usuario__cpf', 'loja__nome']
    inlines = [CarrinhoProdutoInline]
