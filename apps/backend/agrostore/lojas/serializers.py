from django.db import transaction
from rest_framework import serializers

from agrostore.main.campos import CampoImagemUnica
from agrostore.main.imagens import remover_arquivo_apos_commit
from .models import Loja


PASTA_IMAGEM_LOJA = 'lojas'


def remover_imagem_loja_apos_commit(loja, nome):
    # O arquivo só sai do storage se, após o commit, nenhuma outra loja usar o mesmo nome.
    def em_uso():
        return Loja.objects.filter(imagem_perfil=nome).exclude(pk=loja.pk).exists()

    remover_arquivo_apos_commit(loja.imagem_perfil.storage, nome, PASTA_IMAGEM_LOJA, em_uso=em_uso)


class LojaSerializer(serializers.ModelSerializer):
    proprietario_nome = serializers.StringRelatedField(source='proprietario', read_only=True)
    imagem_perfil = CampoImagemUnica(pasta=PASTA_IMAGEM_LOJA)
    # Em multipart, o BooleanField ausente vira False; o default mantém a loja ativa na criação.
    ativa = serializers.BooleanField(default=True)

    class Meta:
        model = Loja
        fields = [
            'loja_id',
            'proprietario',
            'proprietario_nome',
            'nome',
            'descricao',
            'cnpj',
            'imagem_perfil',
            'ativa',
        ]
        # proprietario sempre vem do usuário logado.
        read_only_fields = ['proprietario']

    def validate(self, data):
        usuario = self.context['request'].user
        if not usuario.is_produtor:
            raise serializers.ValidationError("Usuário precisa ser produtor para criar uma loja.")
        if not self.instance and usuario.lojas.exists():
            raise serializers.ValidationError("Cada produtor pode possuir somente uma loja.")
        return data

    def update(self, instance, validated_data):
        nome_anterior = instance.imagem_perfil.name if 'imagem_perfil' in validated_data else ''
        with transaction.atomic():
            loja = super().update(instance, validated_data)
            if nome_anterior and nome_anterior != loja.imagem_perfil.name:
                remover_imagem_loja_apos_commit(loja, nome_anterior)
        return loja
