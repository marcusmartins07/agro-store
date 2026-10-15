# DB-010 (SCRUM-29), etapa 2 de 3: somente dados.
# Fica separada das alterações de schema porque, no PostgreSQL, atualizar uma FK (constraint DEFERRABLE) e
# alterar a mesma tabela na mesma transação gera "cannot ALTER TABLE ... because it has pending trigger events".

from django.db import migrations

LIMITE_IDS_NA_MENSAGEM = 20


def copiar_usuario_para_snapshot(apps, schema_editor):
    Pedido = apps.get_model('pedidos', 'Pedido')
    PedidoCliente = apps.get_model('pedidos', 'PedidoCliente')

    pedidos_sem_snapshot = list(
        Pedido.objects.filter(cliente__isnull=True).order_by('pedido_id').values_list('pedido_id', flat=True)[:LIMITE_IDS_NA_MENSAGEM]
    )
    if pedidos_sem_snapshot:
        raise RuntimeError(
            'DB-010 interrompida: existem pedidos sem pedido_cliente '
            f'(primeiros ids de pedido: {pedidos_sem_snapshot}). '
            'Nenhum dado foi alterado. O schema da 0003 já está aplicado (estado intermediário seguro): '
            'crie o pedido_cliente desses pedidos e rode o migrate novamente.'
        )

    # update() não aciona auto_now: a data_atualizacao do snapshot é preservada.
    for pedido_id, usuario_id in Pedido.objects.values_list('pedido_id', 'usuario_id'):
        PedidoCliente.objects.filter(pedido_id=pedido_id).update(usuario_id=usuario_id)

    if PedidoCliente.objects.filter(usuario__isnull=True).exists():
        raise RuntimeError('DB-010 interrompida: há pedido_cliente sem usuário após a cópia. Nenhum dado foi alterado.')


def devolver_usuario_ao_pedido(apps, schema_editor):
    Pedido = apps.get_model('pedidos', 'Pedido')
    PedidoCliente = apps.get_model('pedidos', 'PedidoCliente')

    for pedido_id, usuario_id in PedidoCliente.objects.values_list('pedido_id', 'usuario_id'):
        Pedido.objects.filter(pedido_id=pedido_id).update(usuario_id=usuario_id)

    pedidos_sem_usuario = list(
        Pedido.objects.filter(usuario__isnull=True).order_by('pedido_id').values_list('pedido_id', flat=True)[:LIMITE_IDS_NA_MENSAGEM]
    )
    if pedidos_sem_usuario:
        raise RuntimeError(
            'Reversão da DB-010 interrompida: existem pedidos sem pedido_cliente para recuperar o usuário '
            f'(primeiros ids de pedido: {pedidos_sem_usuario}). Nenhum dado foi alterado.'
        )


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0003_pedidocliente_usuario'),
    ]

    operations = [
        migrations.RunPython(copiar_usuario_para_snapshot, devolver_usuario_ao_pedido),
    ]
