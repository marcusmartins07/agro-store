from datetime import date

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework import serializers

from agrostore.main.campos import CampoImagemUnica
from agrostore.main.imagens import remover_arquivo_apos_commit
from . import telefones as servico_telefones
from .models import Genero, Telefone, TipoTelefone, Usuario
from .telefones import somente_digitos


PASTA_FOTO_USUARIO = 'usuarios'


def cpf_valido(cpf):
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    for indice in (9, 10):
        soma = sum(int(digito) * (indice + 1 - posicao) for posicao, digito in enumerate(cpf[:indice]))
        digito_verificador = (soma * 10 % 11) % 10
        if digito_verificador != int(cpf[indice]):
            return False
    return True


def validar_genero(valor):
    opcoes = {'M': 'Masculino', 'F': 'Feminino', 'I': 'Indefinido'}
    descricao = opcoes.get(valor)
    if not descricao:
        raise serializers.ValidationError('Informe uma opção de gênero válida.')
    genero = Genero.objects.filter(id_genero=valor).first()
    genero = genero or Genero.objects.filter(genero=descricao).first()
    if not genero:
        raise serializers.ValidationError('A opção de gênero não está disponível.')
    return genero


def validar_data_nascimento(valor):
    hoje = date.today()
    idade = hoje.year - valor.year - ((hoje.month, hoje.day) < (valor.month, valor.day))
    if valor > hoje or idade < 16:
        raise serializers.ValidationError('É necessário ter pelo menos 16 anos para criar uma conta.')
    return valor


def validar_email_unico(valor, usuario_atual=None):
    email = Usuario.objects.normalize_email(valor).lower()
    usuarios = Usuario.objects.filter(email__iexact=email)
    if usuario_atual is not None:
        usuarios = usuarios.exclude(pk=usuario_atual.pk)
    if usuarios.exists():
        raise serializers.ValidationError('Já existe uma conta cadastrada com este e-mail.')
    return email


def validar_nova_senha(senha, confirmacao, usuario):
    """Validações de senha do cadastro, reaproveitadas na redefinição de senha."""
    if senha != confirmacao:
        raise serializers.ValidationError({'password_confirmacao': 'As senhas não coincidem.'})
    try:
        validate_password(senha, usuario)
    except DjangoValidationError as erro:
        raise serializers.ValidationError({'password': erro.messages}) from erro


class TipoTelefoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoTelefone
        fields = ['id', 'descricao']


class TelefoneSerializer(serializers.ModelSerializer):
    """Telefone do próprio usuário. O dono vem sempre do usuário autenticado, nunca do corpo da requisição."""

    numero = serializers.CharField(max_length=20)
    tipo = serializers.PrimaryKeyRelatedField(
        queryset=TipoTelefone.objects.all(),
        error_messages={
            'does_not_exist': servico_telefones.MENSAGEM_TIPO_INDISPONIVEL,
            'incorrect_type': servico_telefones.MENSAGEM_TIPO_INDISPONIVEL,
        },
    )
    tipo_descricao = serializers.CharField(source='tipo.descricao', read_only=True)
    e_principal = serializers.BooleanField(required=False)

    class Meta:
        model = Telefone
        fields = ['id', 'numero', 'tipo', 'tipo_descricao', 'e_principal']

    def validate(self, attrs):
        if 'numero' in attrs or 'tipo' in attrs:
            numero = attrs.get('numero', getattr(self.instance, 'numero', ''))
            tipo = attrs.get('tipo', getattr(self.instance, 'tipo', None))
            try:
                attrs['numero'] = servico_telefones.validar_numero_por_tipo(numero, tipo)
            except servico_telefones.RegraTelefoneViolada as erro:
                raise serializers.ValidationError({'numero': str(erro)}) from erro
        if self.instance is not None and attrs.get('e_principal') is False and self.instance.e_principal:
            raise serializers.ValidationError({'e_principal': servico_telefones.MENSAGEM_DESMARCAR_PRINCIPAL})
        return attrs


class UsuarioPerfilSerializer(serializers.ModelSerializer):
    idade = serializers.ReadOnlyField()
    tem_loja = serializers.SerializerMethodField()
    genero = serializers.SerializerMethodField()
    foto_perfil = CampoImagemUnica(pasta=PASTA_FOTO_USUARIO, read_only=True)
    telefones = TelefoneSerializer(many=True, read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id',
            'nome',
            'cpf',
            'email',
            'telefones',
            'data_nascimento',
            'genero',
            'foto_perfil',
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
    telefone = serializers.CharField(max_length=20, write_only=True)
    tipo_telefone = serializers.PrimaryKeyRelatedField(
        queryset=TipoTelefone.objects.all(),
        write_only=True,
        error_messages={
            'does_not_exist': servico_telefones.MENSAGEM_TIPO_INDISPONIVEL,
            'incorrect_type': servico_telefones.MENSAGEM_TIPO_INDISPONIVEL,
        },
    )
    genero = serializers.CharField(max_length=2)
    password = serializers.CharField(write_only=True, min_length=8, trim_whitespace=False)
    password_confirmacao = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = Usuario
        fields = [
            'nome', 'cpf', 'email', 'telefone', 'tipo_telefone', 'data_nascimento', 'genero', 'password', 'password_confirmacao',
        ]

    def validate_cpf(self, valor):
        cpf = somente_digitos(valor)
        if not cpf_valido(cpf):
            raise serializers.ValidationError('Informe um CPF válido.')
        if Usuario.objects.filter(cpf=cpf).exists():
            raise serializers.ValidationError('Já existe uma conta cadastrada com este CPF.')
        return cpf

    def validate_email(self, valor):
        return validar_email_unico(valor)

    def validate_genero(self, valor):
        return validar_genero(valor)

    def validate_data_nascimento(self, valor):
        return validar_data_nascimento(valor)

    def validate(self, attrs):
        erros = {}
        try:
            attrs['telefone'] = servico_telefones.validar_numero_por_tipo(attrs['telefone'], attrs['tipo_telefone'])
        except servico_telefones.RegraTelefoneViolada as erro:
            erros['telefone'] = [str(erro)]
        usuario = Usuario(
            nome=attrs['nome'],
            cpf=attrs['cpf'],
            email=attrs['email'],
        )
        try:
            validar_nova_senha(attrs['password'], attrs['password_confirmacao'], usuario)
        except serializers.ValidationError as erro:
            erros.update(erro.detail)
        if erros:
            raise serializers.ValidationError(erros)
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirmacao')
        password = validated_data.pop('password')
        numero = validated_data.pop('telefone')
        tipo = validated_data.pop('tipo_telefone')
        with transaction.atomic():
            usuario = Usuario.objects.create_user(password=password, **validated_data)
            servico_telefones.criar_telefone(usuario, numero, tipo, e_principal=True)
        return usuario


class UsuarioAtualizacaoSerializer(serializers.ModelSerializer):
    """Dados pessoais editáveis no perfil. CPF e papéis do usuário não são alterados por aqui."""

    email = serializers.EmailField(max_length=254)
    genero = serializers.CharField(max_length=2)
    foto_perfil = CampoImagemUnica(pasta=PASTA_FOTO_USUARIO)

    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'data_nascimento', 'genero', 'foto_perfil']

    def validate_email(self, valor):
        return validar_email_unico(valor, usuario_atual=self.instance)

    def validate_genero(self, valor):
        return validar_genero(valor)

    def validate_data_nascimento(self, valor):
        return validar_data_nascimento(valor)

    def update(self, instance, validated_data):
        nome_anterior = instance.foto_perfil.name if 'foto_perfil' in validated_data else ''
        with transaction.atomic():
            usuario = super().update(instance, validated_data)
            if nome_anterior and nome_anterior != usuario.foto_perfil.name:
                remover_arquivo_apos_commit(usuario.foto_perfil.storage, nome_anterior, PASTA_FOTO_USUARIO)
        return usuario


class LoginSerializer(serializers.Serializer):
    cpf = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(cpf=somente_digitos(data['cpf']), password=data['password'])
        if not user:
            raise serializers.ValidationError('CPF ou senha inválidos.')
        data['user'] = user
        return data


class SolicitacaoRedefinicaoSenhaSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)


class ConfirmacaoRedefinicaoSenhaSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=128)
    password = serializers.CharField(min_length=8, trim_whitespace=False)
    password_confirmacao = serializers.CharField(trim_whitespace=False)
