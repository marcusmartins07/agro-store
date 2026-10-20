from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms.models import BaseInlineFormSet

from . import telefones as servico_telefones
from .models import Genero, RedefinicaoSenha, Telefone, Usuario


class TelefoneAdminForm(forms.ModelForm):
    principal = forms.BooleanField(label='Principal', required=False)
    numero = forms.CharField(label='Número', max_length=20)

    class Meta:
        model = Telefone
        fields = ['tipo', 'numero']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['principal'].initial = self.instance.e_principal

    def clean(self):
        dados = super().clean()
        tipo = dados.get('tipo')
        numero = dados.get('numero')
        alterou_numero_ou_tipo = self.instance.pk is None or {'tipo', 'numero'} & set(self.changed_data)
        if tipo is not None and numero is not None and alterou_numero_ou_tipo:
            try:
                dados['numero'] = servico_telefones.validar_numero_por_tipo(numero, tipo)
            except servico_telefones.RegraTelefoneViolada as erro:
                self.add_error('numero', str(erro))
        return dados


class TelefoneInlineFormSet(BaseInlineFormSet):
    """Ao salvar o usuário, ao menos 1 telefone e exatamente 1 principal."""

    def clean(self):
        super().clean()
        if any(self.errors):
            return
        restantes = [
            form for form in self.forms
            if form.cleaned_data and not form.cleaned_data.get('DELETE')
        ]
        if not restantes:
            raise ValidationError(servico_telefones.MENSAGEM_ULTIMO_TELEFONE)
        principais = [form for form in restantes if form.cleaned_data.get('principal')]
        if len(principais) != 1:
            raise ValidationError('Marque exatamente um telefone como principal.')


class TelefoneInline(admin.TabularInline):
    model = Telefone
    form = TelefoneAdminForm
    formset = TelefoneInlineFormSet
    extra = 0
    min_num = 1
    validate_min = True


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'email', 'is_produtor', 'is_active']
    list_filter = ['is_produtor', 'is_active']
    search_fields = ['nome', 'cpf', 'email', 'telefones__numero']
    readonly_fields = ['password', 'last_login']
    inlines = [TelefoneInline]

    def save_formset(self, request, form, formset, change):
        if formset.model is not Telefone:
            super().save_formset(request, form, formset, change)
            return

        with transaction.atomic():
            telefone_principal = None
            for form_telefone in formset.forms:
                if form_telefone.cleaned_data.get('principal') and not form_telefone.cleaned_data.get('DELETE'):
                    telefone_principal = form_telefone.instance
            formset.save()
            if telefone_principal is not None:
                servico_telefones.definir_principal(telefone_principal)


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ['id_genero', 'genero']


@admin.register(RedefinicaoSenha)
class RedefinicaoSenhaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'data_criacao', 'data_expiracao', 'data_utilizacao']
    search_fields = ['usuario__nome', 'usuario__email']
    fields = ['usuario', 'data_criacao', 'data_expiracao', 'data_utilizacao']
    readonly_fields = fields

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
