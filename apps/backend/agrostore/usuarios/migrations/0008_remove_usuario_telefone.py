# DB-018 (SCRUM-133), etapa 3 de 3: remove o telefone único do usuário, já copiado para Telefone na 0007.
# A reversão recria a coluna vazia; a reversão da 0007 devolve o telefone principal.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0007_popular_tipos_e_copiar_telefones'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='telefone',
        ),
    ]
