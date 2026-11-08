import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('produtos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('favorito_id', models.BigAutoField(db_column='id_favorito', primary_key=True, serialize=False)),
                ('produto', models.ForeignKey(
                    db_column='id_produto',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='favoritos',
                    to='produtos.produto',
                )),
                ('usuario', models.ForeignKey(
                    db_column='id_usuario',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='favoritos',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'db_table': 'favorito',
                'unique_together': {('usuario', 'produto')},
            },
        ),
    ]
