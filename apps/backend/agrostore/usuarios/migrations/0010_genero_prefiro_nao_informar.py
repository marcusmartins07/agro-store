from django.db import migrations

GENEROS = (
    ('M', 'Masculino', ('Masculino',)),
    ('F', 'Feminino', ('Feminino',)),
    ('I', 'Prefiro não informar', ('Indefinido', 'Prefiro não informar')),
)


def normalizar_generos(apps, schema_editor):
    genero_model = apps.get_model('usuarios', 'Genero')
    usuario_model = apps.get_model('usuarios', 'Usuario')
    for codigo, nome, nomes_equivalentes in GENEROS:
        legados = list(genero_model.objects.filter(genero__in=nomes_equivalentes).exclude(id_genero=codigo))
        for legado in legados:
            legado.genero = f'legado-{legado.id_genero}'
            legado.save(update_fields=['genero'])
        genero_model.objects.update_or_create(id_genero=codigo, defaults={'genero': nome})
        for legado in legados:
            usuario_model.objects.filter(genero_id=legado.id_genero).update(genero_id=codigo)
            legado.delete()


def reverter_nome_indefinido(apps, schema_editor):
    genero_model = apps.get_model('usuarios', 'Genero')
    genero_model.objects.filter(id_genero='I', genero='Prefiro não informar').update(genero='Indefinido')


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0009_nomes_fisicos_modelo_logico'),
    ]

    operations = [
        migrations.RunPython(normalizar_generos, reverter_nome_indefinido),
    ]
