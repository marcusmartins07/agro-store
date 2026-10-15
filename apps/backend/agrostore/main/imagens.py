import uuid
from pathlib import Path


EXTENSOES_IMAGEM = ['jpg', 'jpeg', 'png', 'webp']


def nome_arquivo_aleatorio(pasta, nome_arquivo):
    # Nome aleatório evita colisões e não expõe o nome original do arquivo enviado.
    extensao = Path(nome_arquivo).suffix.lower()
    return f'{pasta}/{uuid.uuid4().hex}{extensao}'
