import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0004_copiar_usuario_para_pedidocliente'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidocliente',
            name='usuario',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='pedidos_cliente',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='usuario',
        ),
        migrations.AlterField(
            model_name='pedido',
            name='loja',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='pedidos',
                to='lojas.loja',
            ),
        ),
    ]
