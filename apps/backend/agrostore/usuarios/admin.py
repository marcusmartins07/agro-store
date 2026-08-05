from django.contrib import admin

from .models import Genero, Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'email', 'telefone', 'is_produtor', 'is_active']
    list_filter = ['is_produtor', 'is_active']
    search_fields = ['nome', 'cpf', 'email', 'telefone']
    readonly_fields = ['password', 'last_login']


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ['id_genero', 'genero']
