from rest_framework import serializers
from rest_framework.utils import html

from .imagens import MENSAGEM_IMAGEM_INVALIDA, nome_gerenciado, validar_imagem_enviada


class CampoImagemUnica(serializers.FileField):
    """Imagem única da loja ou do usuário: sai como URL absoluta, ou null sem imagem válida."""

    def __init__(self, pasta, **kwargs):
        self.pasta = pasta
        kwargs.setdefault('required', False)
        if not kwargs.get('read_only'):
            kwargs.setdefault('validators', [validar_imagem_enviada])
        kwargs['error_messages'] = {
            chave: MENSAGEM_IMAGEM_INVALIDA for chave in ['invalid', 'required', 'null', 'empty', 'no_name']
        }
        super().__init__(**kwargs)

    def get_value(self, dictionary):
        if html.is_html_input(dictionary) and dictionary.get(self.field_name) == '':
            return ''
        return super().get_value(dictionary)

    def to_representation(self, valor):
        if not valor or not nome_gerenciado(valor.name, self.pasta):
            return None
        url = valor.url
        request = self.context.get('request')
        return request.build_absolute_uri(url) if request else url
