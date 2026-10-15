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
        # proprietario sempre vem do usuário logado. imagem_perfil fica somente leitura provisoriamente,
        # até a BE-018 trazer a validação da RN-018 (5 MB e conteúdo) e a checagem do dono da loja.
        read_only_fields = ['proprietario', 'imagem_perfil']

    def validate(self, data):
        usuario = self.context['request'].user
        if not usuario.is_produtor:
            raise serializers.ValidationError("Usuário precisa ser produtor para criar uma loja.")
        if not self.instance and usuario.lojas.exists():
            raise serializers.ValidationError("Cada produtor pode possuir somente uma loja.")
        return data
