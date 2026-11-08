import agrostore.produtos.models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lojas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('categoria_id', models.BigAutoField(db_column='id_categoria', primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100, unique=True)),
                ('ativo', models.BooleanField(db_column='esta_ativa', default=True)),
            ],
            options={
                'db_table': 'categoria',
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('produto_id', models.BigAutoField(db_column='id_produto', default=None, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=155)),
                ('descricao', models.TextField(blank=True)),
                ('codigo_barras', models.CharField(blank=True, max_length=13)),
                ('estoque', models.IntegerField(default=0)),
                ('sku', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('ativo', models.BooleanField(db_column='esta_ativo', default=True)),
                ('categoria', models.ForeignKey(db_column='id_categoria', on_delete=django.db.models.deletion.PROTECT, to='produtos.categoria')),
                ('loja', models.ForeignKey(
                    db_column='id_loja',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='produtos',
                    to='lojas.loja',
                )),
            ],
            options={
                'db_table': 'produto',
            },
        ),
        migrations.CreateModel(
            name='PrecoProduto',
            fields=[
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('id', models.BigAutoField(db_column='id_preco_produto', primary_key=True, serialize=False)),
                ('preco_venda', models.DecimalField(db_column='valor_venda', decimal_places=2, max_digits=10)),
                ('preco_custo', models.DecimalField(blank=True, db_column='valor_custo', decimal_places=2, max_digits=10, null=True)),
                ('preco_desconto', models.DecimalField(blank=True, db_column='valor_desconto', decimal_places=2, max_digits=10, null=True)),
                ('porcentagem_desconto', models.IntegerField(blank=True, null=True)),
                ('vigencia_inicio', models.DateTimeField(default=django.utils.timezone.now)),
                ('vigencia_fim', models.DateTimeField(blank=True, null=True)),
                ('produto', models.ForeignKey(
                    db_column='id_produto',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='precos',
                    to='produtos.produto',
                )),
            ],
            options={
                'db_table': 'preco_produto',
            },
        ),
        migrations.CreateModel(
            name='ImagemProduto',
            fields=[
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('id', models.BigAutoField(db_column='id_imagem', primary_key=True, serialize=False)),
                ('imagem', models.FileField(
                    db_column='caminho',
                    max_length=255,
                    upload_to=agrostore.produtos.models.caminho_imagem_produto,
                    validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
                )),
                ('ordem', models.PositiveIntegerField(default=0)),
                ('e_principal', models.BooleanField(default=False)),
                ('produto', models.ForeignKey(
                    db_column='id_produto',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='imagens',
                    to='produtos.produto',
                )),
            ],
            options={
                'db_table': 'imagem',
                'ordering': ['ordem', 'id'],
                'constraints': [
                    models.UniqueConstraint(
                        condition=models.Q(('e_principal', True)),
                        fields=('produto',),
                        name='imagem_principal_unica_por_produto',
                    ),
                ],
            },
        ),
    ]
