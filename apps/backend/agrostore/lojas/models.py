from django.core.validators import FileExtensionValidator
from django.db import models
from agrostore.main.imagens import EXTENSOES_IMAGEM, nome_arquivo_aleatorio
from agrostore.main.models import BaseModel
from agrostore.usuarios.models import Usuario


def caminho_imagem_loja(loja, nome_arquivo):
    return nome_arquivo_aleatorio('lojas', nome_arquivo)


class Loja(BaseModel):
    loja_id = models.AutoField(primary_key=True)
    # PROTECT: produtor com loja não pode ser excluído; o encerramento é feito pela desativação (RN-019).
    proprietario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='lojas', limit_choices_to={'is_produtor': True})
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    cnpj = models.CharField(max_length=14, unique=True)
    # Valores anteriores (caminhos relativos no storage) foram preservados pela migration 0002.
    imagem_perfil = models.FileField(
        upload_to=caminho_imagem_loja,
        max_length=255,
        blank=True,
        validators=[FileExtensionValidator(EXTENSOES_IMAGEM)],
    )
    ativa = models.BooleanField(default=True)

    class Meta:
        constraints = [
            # Decisão v1: cada produtor pode possuir somente uma loja.
            models.UniqueConstraint(fields=['proprietario'], name='uq_loja_proprietario'),
        ]

    def __str__(self):
        return self.nome