import agrostore.lojas.models
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Loja',
            fields=[
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('loja_id', models.BigAutoField(db_column='id_loja', primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=150)),
                ('descricao', models.TextField(blank=True)),
                ('cnpj', models.CharField(max_length=14, unique=True)),
                ('imagem_perfil', models.FileField(
                    blank=True,
                    max_length=255,
                    upload_to=agrostore.lojas.models.caminho_imagem_loja,
                    validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
                )),
                ('ativa', models.BooleanField(db_column='esta_ativa', default=True)),
                ('proprietario', models.ForeignKey(
                    db_column='id_proprietario',
                    limit_choices_to={'is_produtor': True},
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='lojas',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'db_table': 'loja',
                'constraints': [models.UniqueConstraint(fields=('proprietario',), name='uq_loja_proprietario')],
            },
        ),
    ]
