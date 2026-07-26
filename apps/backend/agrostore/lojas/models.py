from django.db import models
from agrostore.main.models import BaseModel
from agrostore.usuarios.models import Usuario


class Loja(BaseModel):
    loja_id = models.AutoField(primary_key=True)
    proprietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='lojas', limit_choices_to={'is_produtor': True})
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    cnpj = models.CharField(max_length=14, unique=True)
    imagem_perfil = models.CharField(max_length=255, blank=True)
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.nome