import agrostore.usuarios.models
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id_genero', models.CharField(db_column='codigo_genero', max_length=2, primary_key=True, serialize=False)),
                ('genero', models.CharField(db_column='nome', max_length=55, unique=True)),
            ],
            options={
                'db_table': 'genero',
            },
        ),
        migrations.CreateModel(
            name='TipoTelefone',
            fields=[
                ('id', models.BigAutoField(db_column='id_tipo_telefone', primary_key=True, serialize=False)),
                ('descricao', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name': 'tipo de telefone',
                'verbose_name_plural': 'tipos de telefone',
                'db_table': 'tipo_telefone',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(db_column='id_usuario', primary_key=True, serialize=False)),
                ('password', models.CharField(db_column='senha', max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, db_column='ultimo_login', null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(
                    db_column='e_superusuario',
                    default=False,
                    help_text='Designates that this user has all permissions without explicitly assigning them.',
                    verbose_name='superuser status',
                )),
                ('nome', models.CharField(max_length=150)),
                ('cpf', models.CharField(max_length=11, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('data_nascimento', models.DateField()),
                ('foto_perfil', models.FileField(
                    blank=True,
                    max_length=255,
                    upload_to=agrostore.usuarios.models.caminho_foto_usuario,
                    validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
                )),
                ('is_produtor', models.BooleanField(db_column='e_produtor', default=False)),
                ('is_active', models.BooleanField(db_column='esta_ativo', default=True)),
                ('is_staff', models.BooleanField(db_column='e_equipe', default=False)),
                ('groups', models.ManyToManyField(
                    blank=True,
                    help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                    related_name='user_set',
                    related_query_name='user',
                    to='auth.group',
                    verbose_name='groups',
                )),
                ('user_permissions', models.ManyToManyField(
                    blank=True,
                    help_text='Specific permissions for this user.',
                    related_name='user_set',
                    related_query_name='user',
                    to='auth.permission',
                    verbose_name='user permissions',
                )),
                ('genero', models.ForeignKey(db_column='codigo_genero', on_delete=django.db.models.deletion.RESTRICT, to='usuarios.genero')),
            ],
            options={
                'db_table': 'usuario',
            },
        ),
        migrations.CreateModel(
            name='RedefinicaoSenha',
            fields=[
                ('id', models.BigAutoField(db_column='id_redefinicao', primary_key=True, serialize=False)),
                ('token_hash', models.CharField(max_length=64, unique=True)),
                ('data_expiracao', models.DateTimeField()),
                ('data_utilizacao', models.DateTimeField(blank=True, null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(
                    db_column='id_usuario',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='redefinicoes_senha',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'verbose_name': 'redefinição de senha',
                'verbose_name_plural': 'redefinições de senha',
                'db_table': 'redefinicao_senha',
                'ordering': ['-data_criacao'],
                'constraints': [
                    models.CheckConstraint(
                        condition=models.Q(('data_expiracao__gt', models.F('data_criacao'))),
                        name='redefinicao_senha_expiracao_apos_criacao',
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name='Telefone',
            fields=[
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('id', models.BigAutoField(db_column='id_telefone', primary_key=True, serialize=False)),
                ('numero', models.CharField(max_length=11)),
                ('e_principal', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(
                    db_column='id_usuario',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='telefones',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('tipo', models.ForeignKey(
                    db_column='id_tipo_telefone',
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='telefones',
                    to='usuarios.tipotelefone',
                )),
            ],
            options={
                'verbose_name': 'telefone',
                'verbose_name_plural': 'telefones',
                'db_table': 'telefone',
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
