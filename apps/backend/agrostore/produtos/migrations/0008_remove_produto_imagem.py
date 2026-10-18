from django.db import migrations

LIMITE_IDS_NA_MENSAGEM = 20


def verificar_imagens_legadas(apps, schema_editor):
    Produto = apps.get_model('produtos', 'Produto')
    ImagemProduto = apps.get_model('produtos', 'ImagemProduto')

    sem_correspondencia = [
        produto.produto_id
        for produto in Produto.objects.exclude(imagem='').order_by('produto_id')
        if not ImagemProduto.objects.filter(produto_id=produto.produto_id, imagem=produto.imagem.name).exists()
    ]
    if sem_correspondencia:
        raise RuntimeError(
            'DB-019 interrompida: existem produtos com Produto.imagem sem imagem correspondente em ImagemProduto '
            f'({len(sem_correspondencia)} produto(s); primeiros ids: {sem_correspondencia[:LIMITE_IDS_NA_MENSAGEM]}). '
            'Nenhum dado foi alterado. Copie a imagem legada para ImagemProduto e rode o migrate novamente.'
        )


def restaurar_imagem_principal(apps, schema_editor):
    Produto = apps.get_model('produtos', 'Produto')
    ImagemProduto = apps.get_model('produtos', 'ImagemProduto')

    for imagem in ImagemProduto.objects.filter(e_principal=True):
        Produto.objects.filter(produto_id=imagem.produto_id).update(imagem=imagem.imagem.name)


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0007_nomes_fisicos_modelo_logico'),
    ]

    operations = [
        migrations.RunPython(verificar_imagens_legadas, restaurar_imagem_principal),
        migrations.RemoveField(
            model_name='produto',
            name='imagem',
        ),
    ]
