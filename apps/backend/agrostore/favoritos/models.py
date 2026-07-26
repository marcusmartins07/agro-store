from django.db import models
from agrostore.main.models import BaseModel
from agrostore.usuarios.models import Usuario
from agrostore.produtos.models import Produto


class Favorito(BaseModel):
    favorito_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='favoritos')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='favoritos')

    class Meta:
        unique_together = ('usuario', 'produto')  # mesmo produto não duplica

    def __str__(self):
        return f"{self.usuario.nome} - {self.produto.nome}"