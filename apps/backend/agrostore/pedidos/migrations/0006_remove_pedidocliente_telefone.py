# DB-018 (SCRUM-133), RN-021: o telefone deixa de fazer parte do snapshot do cliente.
# Perda aprovada: a reversão recria a coluna vazia, sem os números antigos (restauráveis só pelo backup).
# Sem dependência de usuarios: nenhum app pode depender de pedidos/0003+ (ver pedidos/tests_migrations.py).

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0005_remover_pedido_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedidocliente',
            name='telefone',
        ),
    ]
