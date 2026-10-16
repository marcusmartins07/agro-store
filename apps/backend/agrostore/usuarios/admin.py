from django.contrib import admin

from .models import Genero, RedefinicaoSenha, Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'email', 'telefone', 'is_produtor', 'is_active']
    list_filter = ['is_produtor', 'is_active']
    search_fields = ['nome', 'cpf', 'email', 'telefone']
    readonly_fields = ['password', 'last_login']


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ['id_genero', 'genero']


@admin.register(RedefinicaoSenha)
class RedefinicaoSenhaAdmin(admin.ModelAdmin):
    # Somente leitura (RN-020); o token_hash não é exibido. has_delete_permission não é sobrescrito:
    # com CASCADE, negar a exclusão aqui impediria excluir usuários pelo admin.
    list_display = ['usuario', 'data_criacao', 'data_expiracao', 'data_utilizacao']
    search_fields = ['usuario__nome', 'usuario__email']
    fields = ['usuario', 'data_criacao', 'data_expiracao', 'data_utilizacao']
    readonly_fields = fields

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
