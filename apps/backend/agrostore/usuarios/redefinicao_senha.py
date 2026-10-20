"""Fluxo de redefinição de senha: solicitação do link e confirmação da nova senha."""

import hashlib
import logging
import secrets
import smtplib
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone

from .models import RedefinicaoSenha, Usuario


logger = logging.getLogger(__name__)

MENSAGEM_SOLICITACAO = 'Se houver uma conta com este e-mail, enviaremos um link para redefinir a senha.'
MENSAGEM_LINK_INVALIDO = 'Este link de redefinição é inválido ou expirou. Solicite um novo.'
MENSAGEM_SUCESSO = 'Senha redefinida. Entre com a nova senha.'
MENSAGEM_LIMITE = 'Muitas solicitações. Tente novamente mais tarde.'


class LinkRedefinicaoInvalido(Exception):
    """Link inexistente, expirado, já usado ou de conta inativa."""


def gerar_token():
    return secrets.token_urlsafe(32)


def calcular_hash(token):
    return hashlib.sha256(token.encode()).hexdigest()


def montar_link(token):
    return f'{settings.FRONTEND_URL.rstrip("/")}/redefinir-senha#token={token}'


def invalidar_links_pendentes(usuario, agora):
    RedefinicaoSenha.objects.filter(usuario=usuario, data_utilizacao__isnull=True).update(data_utilizacao=agora)


def enviar_email_redefinicao(usuario, token):
    minutos = settings.REDEFINICAO_SENHA_VALIDADE_MINUTOS
    mensagem = (
        f'Olá, {usuario.nome}.\n\n'
        'Recebemos um pedido para redefinir a senha da sua conta no Agro Store.\n'
        f'Para cadastrar uma nova senha, acesse o link abaixo. Ele vale por {minutos} minutos e pode ser usado uma única vez.\n\n'
        f'{montar_link(token)}\n\n'
        'Se você não fez este pedido, ignore este e-mail. Sua senha atual continua a mesma.\n'
    )
    try:
        send_mail('Redefinição de senha do Agro Store', mensagem, None, [usuario.email], fail_silently=False)
    except (smtplib.SMTPException, OSError) as erro:
        logger.error('Falha ao enviar o e-mail de redefinição de senha (usuário %s): %s', usuario.pk, type(erro).__name__)


def solicitar_redefinicao(email):
    """Cria um link novo somente quando existe exatamente uma conta ativa com o e-mail (sem diferenciar maiúsculas)."""
    usuarios = list(Usuario.objects.filter(email__iexact=email.strip(), is_active=True)[:2])
    if len(usuarios) != 1:
        if len(usuarios) > 1:
            logger.warning('Redefinição de senha não enviada: mais de uma conta ativa com o mesmo e-mail.')
        return

    usuario = usuarios[0]
    token = gerar_token()
    with transaction.atomic():
        invalidar_links_pendentes(usuario, timezone.now())
        data_expiracao = timezone.now() + timedelta(minutes=settings.REDEFINICAO_SENHA_VALIDADE_MINUTOS)
        RedefinicaoSenha.objects.create(usuario=usuario, token_hash=calcular_hash(token), data_expiracao=data_expiracao)
        transaction.on_commit(lambda: enviar_email_redefinicao(usuario, token))


def buscar_redefinicao_valida(token):
    redefinicao = (
        RedefinicaoSenha.objects.select_related('usuario')
        .filter(
            token_hash=calcular_hash(token),
            data_utilizacao__isnull=True,
            data_expiracao__gt=timezone.now(),
            usuario__is_active=True,
        )
        .first()
    )
    if redefinicao is None:
        raise LinkRedefinicaoInvalido
    return redefinicao


def confirmar_redefinicao(redefinicao, nova_senha):
    """Marca o link como usado (update condicional) e troca a senha; os demais links pendentes são invalidados."""
    usuario = redefinicao.usuario
    with transaction.atomic():
        agora = timezone.now()
        marcados = RedefinicaoSenha.objects.filter(
            pk=redefinicao.pk,
            data_utilizacao__isnull=True,
            data_expiracao__gt=agora,
        ).update(data_utilizacao=agora)
        if marcados != 1:
            raise LinkRedefinicaoInvalido

        usuario.refresh_from_db(fields=['is_active'])
        if not usuario.is_active:
            raise LinkRedefinicaoInvalido

        usuario.set_password(nova_senha)
        usuario.save(update_fields=['password'])
        invalidar_links_pendentes(usuario, agora)
