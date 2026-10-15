# DB-003 (SCRUM-22) e DB-014 (SCRUM-118): uma loja por produtor no banco e proprietário protegido.
# A guarda roda antes do UNIQUE para interromper com mensagem clara quando há produtor com mais de uma loja;
# nesse caso nada é alterado e o saneamento dos dados deve ser feito antes de rodar o migrate novamente.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.db.models import Count

LIMITE_IDS_NA_MENSAGEM = 20


def verificar_uma_loja_por_produtor(apps, schema_editor):
    Loja = apps.get_model('lojas', 'Loja')

    proprietarios_duplicados = list(
        Loja.objects.values('proprietario_id')
        .annotate(total=Count('loja_id'))
        .filter(total__gt=1)
        .order_by('proprietario_id')
        .values_list('proprietario_id', flat=True)[:LIMITE_IDS_NA_MENSAGEM]
    )
    if proprietarios_duplicados:
        lojas = list(
            Loja.objects.filter(proprietario_id__in=proprietarios_duplicados)
            .order_by('proprietario_id', 'loja_id')
            .values_list('proprietario_id', 'loja_id')
        )
        raise RuntimeError(
            'DB-003 interrompida: existem produtores com mais de uma loja '
            f'(primeiros ids de proprietário: {proprietarios_duplicados}; pares proprietário/loja: {lojas}). '
            'Nenhum dado foi alterado. Deixe no máximo uma loja por produtor e rode o migrate novamente.'
        )


class Migration(migrations.Migration):

    dependencies = [
        ('lojas', '0002_alter_loja_imagem_perfil'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(verificar_uma_loja_por_produtor, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='loja',
            name='proprietario',
            field=models.ForeignKey(
                limit_choices_to={'is_produtor': True},
                on_delete=django.db.models.deletion.PROTECT,
                related_name='lojas',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddConstraint(
            model_name='loja',
            constraint=models.UniqueConstraint(fields=('proprietario',), name='uq_loja_proprietario'),
        ),
    ]
