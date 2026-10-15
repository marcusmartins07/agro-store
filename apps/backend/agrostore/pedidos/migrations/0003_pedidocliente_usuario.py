# DB-010 (SCRUM-29), etapa 1 de 3: somente schema.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0002_pedidocliente_telefone'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidocliente',
            name='usuario',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='pedidos_cliente',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        # Nulo só durante a transição: permite que a reversão da 0005 recrie a coluna em uma tabela com dados.
        migrations.AlterField(
            model_name='pedido',
            name='usuario',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='pedidos',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
