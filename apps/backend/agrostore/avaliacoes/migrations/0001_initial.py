import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pedidos', '0001_initial'),
        ('produtos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('avaliacao_id', models.BigAutoField(db_column='id_avaliacao', primary_key=True, serialize=False)),
                ('nota', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comentario', models.TextField(blank=True)),
                ('pedido_produto', models.OneToOneField(
                    db_column='id_pedido_produto',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='avaliacao',
                    to='pedidos.pedidoproduto',
                )),
                ('produto', models.ForeignKey(
                    blank=True,
                    db_column='id_produto',
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='avaliacoes',
                    to='produtos.produto',
                )),
                ('usuario', models.ForeignKey(
                    db_column='id_usuario',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='avaliacoes',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'db_table': 'avaliacao',
            },
        ),
    ]
