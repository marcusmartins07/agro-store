import sys

from django.db import migrations

TIPOS_TELEFONE = ['Celular', 'Fixo', 'Comercial']


def criar_tipos_telefone(apps, schema_editor):
    TipoTelefone = apps.get_model('usuarios', 'TipoTelefone')
    for descricao in TIPOS_TELEFONE:
        TipoTelefone.objects.get_or_create(descricao=descricao)


def copiar_telefone_do_usuario(apps, schema_editor):
    Usuario = apps.get_model('usuarios', 'Usuario')
    TipoTelefone = apps.get_model('usuarios', 'TipoTelefone')
    Telefone = apps.get_model('usuarios', 'Telefone')

    celular = TipoTelefone.objects.get(descricao='Celular')
    fixo = TipoTelefone.objects.get(descricao='Fixo')
    fora_do_padrao = 0

    usuarios = Usuario.objects.exclude(telefone__isnull=True).exclude(telefone='').only('pk', 'telefone')
    for usuario in usuarios.iterator():
        numero = ''.join(caractere for caractere in usuario.telefone if caractere.isdigit())
        if not numero or Telefone.objects.filter(usuario_id=usuario.pk).exists():
            continue
        if len(numero) == 10:
            tipo = fixo
        else:
            tipo = celular
            if len(numero) != 11:
                fora_do_padrao += 1
        Telefone.objects.create(usuario_id=usuario.pk, tipo=tipo, numero=numero, e_principal=True)

    if fora_do_padrao:
        sys.stdout.write(
            f'\n  DB-018: {fora_do_padrao} telefone(s) fora do padrão gravados como Celular; '
            'liste-os com "python manage.py telefones_fora_do_padrao".\n'
        )


def devolver_telefone_principal(apps, schema_editor):
    Usuario = apps.get_model('usuarios', 'Usuario')
    Telefone = apps.get_model('usuarios', 'Telefone')

    for telefone in Telefone.objects.filter(e_principal=True).iterator():
        Usuario.objects.filter(pk=telefone.usuario_id).update(telefone=telefone.numero)
    Telefone.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_tipotelefone_telefone'),
    ]

    operations = [
        migrations.RunPython(criar_tipos_telefone, migrations.RunPython.noop),
        migrations.RunPython(copiar_telefone_do_usuario, devolver_telefone_principal),
    ]
