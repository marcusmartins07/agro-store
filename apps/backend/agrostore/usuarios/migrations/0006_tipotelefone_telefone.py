import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0005_redefinicaosenha'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoTelefone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name': 'tipo de telefone',
                'verbose_name_plural': 'tipos de telefone',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Telefone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('numero', models.CharField(max_length=11)),
                ('e_principal', models.BooleanField(default=False)),
                ('tipo', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT, related_name='telefones', to='usuarios.tipotelefone',
                )),
                ('usuario', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, related_name='telefones', to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'verbose_name': 'telefone',
                'verbose_name_plural': 'telefones',
                'ordering': ['-e_principal', 'id'],
                'constraints': [
                    models.UniqueConstraint(
                        condition=models.Q(('e_principal', True)),
                        fields=('usuario',),
                        name='telefone_principal_unico_por_usuario',
                    ),
                ],
            },
        ),
    ]
