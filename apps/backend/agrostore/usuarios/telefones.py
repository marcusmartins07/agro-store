"""Telefones do usuário (RN-021): validação do número por tipo e operações que mantêm um único principal."""

from django.db import transaction

from .models import Telefone, TipoTelefone, Usuario


MENSAGEM_ULTIMO_TELEFONE = 'Você precisa manter ao menos um telefone.'
MENSAGEM_EXCLUIR_PRINCIPAL = 'Defina outro telefone como principal antes de excluir este.'
MENSAGEM_DESMARCAR_PRINCIPAL = 'Defina outro telefone como principal.'
MENSAGEM_TIPO_INDISPONIVEL = 'Informe um tipo de telefone válido.'
MENSAGENS_DIGITOS_POR_TIPO = {
    TipoTelefone.CELULAR: 'Celular deve ter 11 dígitos com DDD.',
    TipoTelefone.FIXO: 'Telefone fixo deve ter 10 dígitos com DDD.',
    TipoTelefone.COMERCIAL: 'Telefone comercial deve ter 10 ou 11 dígitos com DDD.',
}


class RegraTelefoneViolada(Exception):
    """Operação recusada pela RN-021; a mensagem pode ser exibida ao usuário."""


def somente_digitos(valor):
    return ''.join(caractere for caractere in valor if caractere.isdigit())


def numero_respeita_tipo(numero, tipo):
    return len(numero) in TipoTelefone.DIGITOS_POR_TIPO.get(tipo.descricao, ())


def validar_numero_por_tipo(numero, tipo):
    """Devolve o número só com dígitos ou levanta RegraTelefoneViolada se a quantidade não servir para o tipo."""
    if tipo.descricao not in TipoTelefone.DIGITOS_POR_TIPO:
        raise RegraTelefoneViolada(MENSAGEM_TIPO_INDISPONIVEL)
    numero_limpo = somente_digitos(numero or '')
    if not numero_respeita_tipo(numero_limpo, tipo):
        raise RegraTelefoneViolada(MENSAGENS_DIGITOS_POR_TIPO[tipo.descricao])
    return numero_limpo


def _travar_usuario(usuario_id):
    # Serializa as operações de telefone do mesmo usuário (contagem, principal) até o fim da transação.
    Usuario.objects.select_for_update().only('pk').get(pk=usuario_id)


def _desmarcar_principais(usuario_id, exceto_pk=None):
    telefones = Telefone.objects.filter(usuario_id=usuario_id, e_principal=True)
    if exceto_pk is not None:
        telefones = telefones.exclude(pk=exceto_pk)
    telefones.update(e_principal=False)


def criar_telefone(usuario, numero, tipo, e_principal=False):
    """Cria o telefone; o primeiro do usuário vira principal automaticamente (exceção legada)."""
    numero_limpo = validar_numero_por_tipo(numero, tipo)
    with transaction.atomic():
        _travar_usuario(usuario.pk)
        if not Telefone.objects.filter(usuario_id=usuario.pk).exists():
            e_principal = True
        if e_principal:
            _desmarcar_principais(usuario.pk)
        return Telefone.objects.create(usuario=usuario, tipo=tipo, numero=numero_limpo, e_principal=e_principal)


def definir_principal(telefone):
    """Desmarca os demais antes de marcar este, para não violar telefone_principal_unico_por_usuario."""
    with transaction.atomic():
        _travar_usuario(telefone.usuario_id)
        _desmarcar_principais(telefone.usuario_id, exceto_pk=telefone.pk)
        telefone.e_principal = True
        telefone.save(update_fields=['e_principal', 'data_atualizacao'])
    return telefone


def atualizar_telefone(telefone, numero=None, tipo=None, e_principal=None):
    """Edita número e tipo (revalidando o par) e, se pedido, torna o telefone principal; não desmarca o principal."""
    with transaction.atomic():
        _travar_usuario(telefone.usuario_id)
        telefone.refresh_from_db(fields=['numero', 'tipo', 'e_principal'])
        if e_principal is False and telefone.e_principal:
            raise RegraTelefoneViolada(MENSAGEM_DESMARCAR_PRINCIPAL)

        # Só revalida quando número ou tipo são enviados: um legado fora do padrão ainda pode ser definido como principal.
        if numero is not None or tipo is not None:
            novo_tipo = tipo if tipo is not None else telefone.tipo
            novo_numero = numero if numero is not None else telefone.numero
            telefone.numero = validar_numero_por_tipo(novo_numero, novo_tipo)
            telefone.tipo = novo_tipo
            telefone.save(update_fields=['numero', 'tipo', 'data_atualizacao'])
        if e_principal and not telefone.e_principal:
            definir_principal(telefone)
    return telefone


def excluir_telefone(telefone):
    """Não exclui o último telefone nem o principal; não há promoção automática de outro telefone."""
    with transaction.atomic():
        _travar_usuario(telefone.usuario_id)
        telefone.refresh_from_db(fields=['e_principal'])
        if not Telefone.objects.filter(usuario_id=telefone.usuario_id).exclude(pk=telefone.pk).exists():
            raise RegraTelefoneViolada(MENSAGEM_ULTIMO_TELEFONE)
        if telefone.e_principal:
            raise RegraTelefoneViolada(MENSAGEM_EXCLUIR_PRINCIPAL)
        telefone.delete()
