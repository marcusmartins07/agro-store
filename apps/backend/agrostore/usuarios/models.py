from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from datetime import date
from agrostore.main.imagens import EXTENSOES_IMAGEM, nome_arquivo_aleatorio
from agrostore.main.models import BaseModel


def caminho_foto_usuario(usuario, nome_arquivo):
    return nome_arquivo_aleatorio('usuarios', nome_arquivo)


class UsuarioManager(BaseUserManager):

    def create_user(self, cpf, email, password=None, **extra_fields):
        if not cpf:
            raise ValueError("CPF é obrigatório")
        if not email:
            raise ValueError("Email é obrigatório")

        email = self.normalize_email(email)
        user = self.model(cpf=cpf, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(cpf, email, password, **extra_fields)


class Genero(models.Model):
    id_genero = models.CharField(max_length=2, primary_key=True, db_column='codigo_genero')
    genero = models.CharField(max_length=55, unique=True, db_column='nome')

    class Meta:
        db_table = 'genero'

    def __str__(self):
        return self.genero


class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True, db_column='id_usuario')
    password = models.CharField(_('password'), max_length=128, db_column='senha')
    last_login = models.DateTimeField(_('last login'), blank=True, null=True, db_column='ultimo_login')
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_('Designates that this user has all permissions without explicitly assigning them.'),
        db_column='e_superusuario',
    )
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField()
    genero = models.ForeignKey(Genero, on_delete=models.RESTRICT, db_column='codigo_genero')
    foto_perfil = models.FileField(
        upload_to=caminho_foto_usuario,
        max_length=255,
        blank=True,
        validators=[FileExtensionValidator(EXTENSOES_IMAGEM)],
    )
    is_produtor = models.BooleanField(default=False, db_column='e_produtor')
    is_active = models.BooleanField(default=True, db_column='esta_ativo')
    is_staff = models.BooleanField(default=False, db_column='e_equipe')

    objects = UsuarioManager()

    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.nome

    @property
    def idade(self):
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )


class TipoTelefone(models.Model):
    # Tipos fixos (RN-021), carregados pela migration 0007; não são cadastrados pelo usuário.
    CELULAR = 'Celular'
    FIXO = 'Fixo'
    COMERCIAL = 'Comercial'
    DIGITOS_POR_TIPO = {CELULAR: (11,), FIXO: (10,), COMERCIAL: (10, 11)}

    id = models.BigAutoField(primary_key=True, db_column='id_tipo_telefone')
    descricao = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = 'tipo_telefone'
        ordering = ['id']
        verbose_name = 'tipo de telefone'
        verbose_name_plural = 'tipos de telefone'

    def __str__(self):
        return self.descricao


class Telefone(BaseModel):
    # RN-021: o mínimo de 1 telefone e os dígitos por tipo são validados na API e no admin; o banco garante 1 principal no máximo.
    id = models.BigAutoField(primary_key=True, db_column='id_telefone')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='telefones', db_column='id_usuario')
    tipo = models.ForeignKey(TipoTelefone, on_delete=models.PROTECT, related_name='telefones', db_column='id_tipo_telefone')
    numero = models.CharField(max_length=11)
    e_principal = models.BooleanField(default=False)

    class Meta:
        db_table = 'telefone'
        ordering = ['-e_principal', 'id']
        verbose_name = 'telefone'
        verbose_name_plural = 'telefones'
        constraints = [
            models.UniqueConstraint(
                fields=['usuario'],
                condition=models.Q(e_principal=True),
                name='telefone_principal_unico_por_usuario',
            ),
        ]

    def __str__(self):
        return f'{self.tipo} {self.numero}'


class RedefinicaoSenha(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='id_redefinicao')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='redefinicoes_senha', db_column='id_usuario')
    token_hash = models.CharField(max_length=64, unique=True)
    data_expiracao = models.DateTimeField()
    data_utilizacao = models.DateTimeField(null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'redefinicao_senha'
        ordering = ['-data_criacao']
        verbose_name = 'redefinição de senha'
        verbose_name_plural = 'redefinições de senha'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(data_expiracao__gt=models.F('data_criacao')),
                name='redefinicao_senha_expiracao_apos_criacao',
            ),
        ]

    def __str__(self):
        return f'Redefinição de senha #{self.pk}'
