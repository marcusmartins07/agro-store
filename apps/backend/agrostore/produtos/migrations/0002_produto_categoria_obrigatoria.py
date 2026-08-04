from django.db import migrations, models
import django.db.models.deletion


def validar_produtos_categorizados(apps, schema_editor):
    Produto = apps.get_model('produtos', 'Produto')
    if Produto.objects.filter(categoria__isnull=True).exists():
        raise RuntimeError(
            'Há produtos sem categoria. Atribua uma categoria a todos os produtos antes de aplicar esta migration.'
        )


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(validar_produtos_categorizados, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='produto',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='produtos.categoria'),
        ),
    ]
