from rest_framework import serializers
from .models import Loja


class LojaSerializer(serializers.ModelSerializer):
    proprietario_nome = serializers.StringRelatedField(source='proprietario', read_only=True)

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
        read_only_fields = ['proprietario']  # sempre vem do usuário logado

    def validate(self, data):
        if not self.context['request'].user.is_produtor:
            raise serializers.ValidationError("Usuário precisa ser produtor para criar uma loja.")
        return data