from django.contrib import admin

from .models import Avaliacao


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    # Moderação (RN-010): o administrador apenas consulta e exclui avaliações.
    list_display = ['avaliacao_id', 'produto', 'usuario', 'nota', 'data_criacao']
    list_filter = ['nota']
    search_fields = ['produto__nome', 'usuario__nome', 'comentario']
    list_select_related = ['produto', 'usuario']
    raw_id_fields = ['usuario', 'produto', 'pedido_produto']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
