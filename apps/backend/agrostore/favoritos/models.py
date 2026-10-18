from django.db import models
from agrostore.main.models import BaseModel
from agrostore.usuarios.models import Usuario
from agrostore.produtos.models import Produto


class Favorito(BaseModel):
    favorito_id = models.BigAutoField(primary_key=True, db_column='id_favorito')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='favoritos', db_column='id_usuario')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='favoritos', db_column='id_produto')

    class Meta:
        db_table = 'favorito'
        unique_together = ('usuario', 'produto')  # mesmo produto não duplica

    def __str__(self):
        return f"{self.usuario.nome} - {self.produto.nome}"
