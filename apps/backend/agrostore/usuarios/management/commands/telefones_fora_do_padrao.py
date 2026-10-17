from django.core.management.base import BaseCommand

from agrostore.usuarios.models import Telefone
from agrostore.usuarios.telefones import numero_respeita_tipo


class Command(BaseCommand):
    help = (
        'Lista, somente para leitura, os telefones cuja quantidade de dígitos não respeita o tipo (RN-021). '
        'Exibe ids, tipo e quantidade de dígitos, nunca o número.'
    )

    def handle(self, *args, **options):
        fora_do_padrao = [
            telefone
            for telefone in Telefone.objects.select_related('tipo').order_by('usuario_id', 'id').iterator()
            if not numero_respeita_tipo(telefone.numero, telefone.tipo)
        ]
        if not fora_do_padrao:
            self.stdout.write(self.style.SUCCESS('Nenhum telefone fora do padrão.'))
            return

        for telefone in fora_do_padrao:
            self.stdout.write(
                f'usuario={telefone.usuario_id} telefone={telefone.id} tipo={telefone.tipo.descricao} '
                f'digitos={len(telefone.numero)}'
            )
        self.stdout.write(self.style.WARNING(f'{len(fora_do_padrao)} telefone(s) fora do padrão. Corrija pela área administrativa.'))
