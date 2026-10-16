from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
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
    id_genero = models.CharField(max_length=2, primary_key=True)
    genero = models.CharField(max_length=55, unique=True)

    def __str__(self):
        return self.genero


class Usuario(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField()
    genero = models.ForeignKey(Genero, on_delete=models.RESTRICT)
    telefone = models.CharField(max_length=11, null=True, blank=True)
    foto_perfil = models.FileField(
        upload_to=caminho_foto_usuario,
        max_length=255,
        blank=True,
        validators=[FileExtensionValidator(EXTENSOES_IMAGEM)],
    )
    is_produtor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.nome

    @property
    def idade(self):
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )


class RedefinicaoSenha(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='redefinicoes_senha')
    token_hash = models.CharField(max_length=64, unique=True)
    data_expiracao = models.DateTimeField()
    data_utilizacao = models.DateTimeField(null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
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
