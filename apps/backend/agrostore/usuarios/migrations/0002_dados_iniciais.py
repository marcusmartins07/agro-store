from django.db import migrations

GENEROS = [('M', 'Masculino'), ('F', 'Feminino'), ('I', 'Prefiro não informar')]
TIPOS_TELEFONE = ['Celular', 'Fixo', 'Comercial']


def criar_dados_iniciais(apps, schema_editor):
    genero_model = apps.get_model('usuarios', 'Genero')
    tipo_telefone_model = apps.get_model('usuarios', 'TipoTelefone')
    for codigo, nome in GENEROS:
        genero_model.objects.get_or_create(id_genero=codigo, defaults={'genero': nome})
    genero_model.objects.filter(id_genero='I', genero='Indefinido').update(genero='Prefiro não informar')
    for descricao in TIPOS_TELEFONE:
        tipo_telefone_model.objects.get_or_create(descricao=descricao)


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(criar_dados_iniciais, migrations.RunPython.noop),
    ]
