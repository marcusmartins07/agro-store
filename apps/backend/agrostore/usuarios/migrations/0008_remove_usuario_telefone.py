from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0007_popular_tipos_e_copiar_telefones'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='telefone',
        ),
    ]
