import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lojas', '0001_initial'),
        ('produtos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusPedido',
            fields=[
                ('status_pedido_id', models.BigAutoField(db_column='id_status_pedido', primary_key=True, serialize=False)),
                ('status', models.CharField(db_column='nome', max_length=55, unique=True)),
            ],
            options={
                'verbose_name': 'status do pedido',
                'verbose_name_plural': 'status dos pedidos',
                'db_table': 'status_pedido',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('pedido_id', models.BigAutoField(db_column='id_pedido', primary_key=True, serialize=False)),
                ('valor_bruto', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('valor_desconto', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('valor_liquido', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('loja', models.ForeignKey(
                    db_column='id_loja',
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='pedidos',
                    to='lojas.loja',
                )),
                ('status', models.ForeignKey(
                    db_column='id_status_pedido',
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='pedidos',
                    to='pedidos.statuspedido',
                )),
            ],
            options={
                'db_table': 'pedido',
            },
        ),
        migrations.CreateModel(
            name='PedidoCliente',
            fields=[
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('pedido_cliente_id', models.BigAutoField(db_column='id_pedido_cliente', primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=150)),
                ('cpf', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254)),
                ('data_nascimento', models.DateField()),
                ('genero', models.CharField(max_length=55)),
                ('pedido', models.OneToOneField(
                    db_column='id_pedido',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='cliente',
                    to='pedidos.pedido',
                )),
                ('usuario', models.ForeignKey(
                    db_column='id_usuario',
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='pedidos_cliente',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'db_table': 'pedido_cliente',
            },
        ),
        migrations.CreateModel(
            name='PedidoProduto',
            fields=[
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('pedido_produto_id', models.BigAutoField(db_column='id_pedido_produto', primary_key=True, serialize=False)),
                ('nome_produto', models.CharField(max_length=155)),
                ('quantidade', models.PositiveIntegerField()),
                ('valor_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('valor_desconto', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pedido', models.ForeignKey(
                    db_column='id_pedido',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='itens',
                    to='pedidos.pedido',
                )),
                ('produto', models.ForeignKey(
                    blank=True,
                    db_column='id_produto',
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to='produtos.produto',
                )),
            ],
            options={
                'db_table': 'pedido_produto',
                'constraints': [
                    models.CheckConstraint(condition=models.Q(('quantidade__gt', 0)), name='pedido_produto_quantidade_positiva'),
                    models.CheckConstraint(condition=models.Q(('valor_unitario__gte', 0)), name='pedido_produto_valor_unitario_nao_negativo'),
                    models.CheckConstraint(condition=models.Q(('valor_desconto__gte', 0)), name='pedido_produto_valor_desconto_nao_negativo'),
                    models.CheckConstraint(condition=models.Q(('subtotal__gte', 0)), name='pedido_produto_subtotal_nao_negativo'),
                ],
            },
        ),
    ]
