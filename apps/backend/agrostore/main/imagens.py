import logging
import re
import uuid
from pathlib import Path

from botocore.exceptions import BotoCoreError, ClientError
from django.core.exceptions import ValidationError
from django.db import transaction


logger = logging.getLogger(__name__)

EXTENSOES_IMAGEM = ['jpg', 'jpeg', 'png', 'webp']
TAMANHO_MAXIMO_IMAGEM = 5 * 1024 * 1024
ASSINATURAS_IMAGEM = (
    b'\xff\xd8\xff',  # JPEG
    b'\x89PNG\r\n\x1a\n',  # PNG
)
MENSAGEM_IMAGEM_INVALIDA = 'Envie uma imagem JPG, PNG ou WEBP válida.'
MENSAGEM_IMAGEM_GRANDE = 'A imagem deve ter no máximo 5 MB.'


def nome_arquivo_aleatorio(pasta, nome_arquivo):
    # Nome aleatório evita colisões e não expõe o nome original do arquivo enviado.
    extensao = Path(nome_arquivo).suffix.lower()
    return f'{pasta}/{uuid.uuid4().hex}{extensao}'


def arquivo_e_imagem(arquivo):
    arquivo.seek(0)
    cabecalho = arquivo.read(12)
    arquivo.seek(0)
    e_webp = cabecalho[:4] == b'RIFF' and cabecalho[8:12] == b'WEBP'
    return e_webp or cabecalho.startswith(ASSINATURAS_IMAGEM)


def validar_imagem_enviada(arquivo):
    """Validações de arquivo da RN-018 (mesmas da RN-016): extensão, tamanho de até 5 MB e conteúdo."""
    extensao = Path(arquivo.name or '').suffix.lower().lstrip('.')
    if extensao not in EXTENSOES_IMAGEM:
        raise ValidationError(MENSAGEM_IMAGEM_INVALIDA)
    if arquivo.size > TAMANHO_MAXIMO_IMAGEM:
        raise ValidationError(MENSAGEM_IMAGEM_GRANDE)
    if not arquivo_e_imagem(arquivo):
        raise ValidationError(MENSAGEM_IMAGEM_INVALIDA)


def nome_gerenciado(nome, pasta):
    """Indica se o nome segue o padrão gerado pelo sistema; valores legados fora dele são tratados como sem imagem."""
    padrao = rf'{re.escape(pasta)}/[0-9a-f]{{32}}\.({"|".join(EXTENSOES_IMAGEM)})'
    return bool(nome) and re.fullmatch(padrao, nome) is not None


def remover_arquivo_apos_commit(storage, nome, pasta, em_uso=None):
    """Remove o arquivo do storage depois do commit; nomes fora do padrão gerado nunca são apagados."""
    if not nome_gerenciado(nome, pasta):
        return

    def remover():
        if em_uso is not None and em_uso():
            return
        try:
            storage.delete(nome)
        except (OSError, BotoCoreError, ClientError):
            # Falha no storage não desfaz a troca já gravada; o arquivo fica órfão e o erro é registrado sem dados pessoais.
            logger.warning('Falha ao remover arquivo de imagem substituída do storage (pasta %s).', pasta)

    transaction.on_commit(remover)
