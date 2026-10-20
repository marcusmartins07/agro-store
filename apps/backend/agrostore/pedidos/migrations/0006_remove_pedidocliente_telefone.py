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
