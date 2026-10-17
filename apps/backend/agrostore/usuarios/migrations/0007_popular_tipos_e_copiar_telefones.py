# DB-018 (SCRUM-133), etapa 2 de 3: somente dados (RN-021).
# Copia SOMENTE Usuario.telefone para Telefone, como principal. O telefone do snapshot do pedido não é aproveitado.
# Números fora do padrão entram como Celular; a listagem para correção é feita pelo comando telefones_fora_do_padrao
# (somente leitura). Esta migration não imprime ids nem números, apenas uma contagem.

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
        # Valor sem nenhum dígito não gera telefone (exceção legada aprovada: usuário pode ficar com 0 telefones).
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
    # Reversão com perda: só o telefone principal volta para Usuario.telefone; os demais são descartados.
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
        # A tabela de tipos é apagada pela reversão da 0006; não há o que desfazer aqui.
        migrations.RunPython(criar_tipos_telefone, migrations.RunPython.noop),
        migrations.RunPython(copiar_telefone_do_usuario, devolver_telefone_principal),
    ]
