from datetime import date

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Genero, Usuario


def somente_digitos(valor):
    return ''.join(caractere for caractere in valor if caractere.isdigit())


def cpf_valido(cpf):
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    for indice in (9, 10):
        soma = sum(int(digito) * (indice + 1 - posicao) for posicao, digito in enumerate(cpf[:indice]))
        digito_verificador = (soma * 10 % 11) % 10
        if digito_verificador != int(cpf[indice]):
            return False
    return True


class UsuarioPerfilSerializer(serializers.ModelSerializer):
    idade = serializers.ReadOnlyField()
    tem_loja = serializers.SerializerMethodField()
    genero = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = [
            'id',
            'nome',
            'cpf',
            'email',
            'telefone',
            'data_nascimento',
            'genero',
            'is_produtor',
            'tem_loja',
            'idade',
        ]
        read_only_fields = fields

    def get_tem_loja(self, obj):
        return obj.lojas.exists()

    def get_genero(self, obj):
        codigos_por_descricao = {'Masculino': 'M', 'Feminino': 'F', 'Indefinido': 'I'}
        return codigos_por_descricao.get(obj.genero.genero, obj.genero_id)


class CadastroClienteSerializer(serializers.ModelSerializer):
    cpf = serializers.CharField(max_length=14)
    telefone = serializers.CharField(max_length=15)
    genero = serializers.CharField(max_length=2)
    password = serializers.CharField(write_only=True, min_length=8, trim_whitespace=False)
    password_confirmacao = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = Usuario
        fields = ['nome', 'cpf', 'email', 'telefone', 'data_nascimento', 'genero', 'password', 'password_confirmacao']

    def validate_cpf(self, valor):
        cpf = somente_digitos(valor)
        if not cpf_valido(cpf):
            raise serializers.ValidationError('Informe um CPF válido.')
        if Usuario.objects.filter(cpf=cpf).exists():
            raise serializers.ValidationError('Já existe uma conta cadastrada com este CPF.')
        return cpf

    def validate_telefone(self, valor):
        telefone = somente_digitos(valor)
        if len(telefone) != 11:
            raise serializers.ValidationError('Informe um celular brasileiro com 11 dígitos.')
        return telefone

    def validate_email(self, valor):
        email = Usuario.objects.normalize_email(valor).lower()
        if Usuario.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError('Já existe uma conta cadastrada com este e-mail.')
        return email

    def validate_genero(self, valor):
        opcoes = {'M': 'Masculino', 'F': 'Feminino', 'I': 'Indefinido'}
        descricao = opcoes.get(valor)
        if not descricao:
            raise serializers.ValidationError('Informe uma opção de gênero válida.')
        genero = Genero.objects.filter(id_genero=valor).first()
        genero = genero or Genero.objects.filter(genero=descricao).first()
        if not genero:
            raise serializers.ValidationError('A opção de gênero não está disponível.')
        return genero

    def validate_data_nascimento(self, valor):
        hoje = date.today()
        idade = hoje.year - valor.year - ((hoje.month, hoje.day) < (valor.month, valor.day))
        if valor > hoje or idade < 16:
            raise serializers.ValidationError('É necessário ter pelo menos 16 anos para criar uma conta.')
        return valor

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmacao']:
            raise serializers.ValidationError({'password_confirmacao': 'As senhas não coincidem.'})

        usuario = Usuario(
            nome=attrs['nome'],
            cpf=attrs['cpf'],
            email=attrs['email'],
            telefone=attrs['telefone'],
        )
        try:
            validate_password(attrs['password'], usuario)
        except DjangoValidationError as erro:
            raise serializers.ValidationError({'password': erro.messages}) from erro
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirmacao')
        password = validated_data.pop('password')
        return Usuario.objects.create_user(password=password, **validated_data)


class LoginSerializer(serializers.Serializer):
    cpf = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(cpf=somente_digitos(data['cpf']), password=data['password'])
        if not user:
            raise serializers.ValidationError('CPF ou senha inválidos.')
        data['user'] = user
        return data
