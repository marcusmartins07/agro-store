import os
import shutil
import tempfile
from unittest import mock

from botocore.exceptions import ClientError
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, transaction
from django.db.models import ProtectedError
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from agrostore.lojas.models import Loja
from agrostore.lojas.serializers import LojaSerializer
from agrostore.usuarios.models import Genero, Usuario


class LojaAPITests(APITestCase):
    def setUp(self):
        genero, _ = Genero.objects.get_or_create(id_genero='M', defaults={'genero': 'Masculino'})
        self.produtor = Usuario.objects.create_user(
            cpf='98765432100',
            email='loja-produtor@example.com',
            password='senha123',
            nome='Produtor da Loja',
            data_nascimento='1980-01-01',
            genero=genero,
            is_produtor=True,
        )
        self.client.force_authenticate(self.produtor)

    def test_produtor_nao_cria_segunda_loja(self):
        primeira = {'nome': 'Feira Central', 'cnpj': '98765432000199'}
        segunda = {'nome': 'Feira da Praça', 'cnpj': '98765432000198'}

        response = self.client.post('/api/v1/lojas/lojas/', primeira, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/api/v1/lojas/lojas/', segunda, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_produtor_atualiza_apenas_nome_descricao_e_status_da_loja(self):
        self.client.post('/api/v1/lojas/lojas/', {'nome': 'Feira Central', 'cnpj': '98765432000199'}, format='json')

        response = self.client.patch('/api/v1/lojas/me/', {'descricao': 'Produtos da estação', 'ativa': False}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['descricao'], 'Produtos da estação')
        self.assertFalse(response.data['ativa'])

        response = self.client.patch('/api/v1/lojas/me/', {'nome': 'Sítio Boa Terra'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Sítio Boa Terra')

        response = self.client.patch('/api/v1/lojas/me/', {'nome': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.patch('/api/v1/lojas/me/', {'cnpj': '98765432000198'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LojaImagemPerfilModelTests(TestCase):
    def setUp(self):
        genero, _ = Genero.objects.get_or_create(id_genero='M', defaults={'genero': 'Masculino'})
        self.produtor = Usuario.objects.create_user(
            cpf='98765432111', email='loja-model@example.com', password='senha123',
            nome='Produtor Model', data_nascimento='1980-01-01', genero=genero, is_produtor=True,
        )

    def montar_loja(self, imagem=''):
        loja = Loja(proprietario=self.produtor, nome='Feira Model', cnpj='98765432000111')
        if imagem:
            loja.imagem_perfil.name = imagem
        return loja

    def test_loja_sem_imagem_e_valida_e_guarda_texto_vazio(self):
        loja = self.montar_loja()
        loja.full_clean()
        loja.save()
        loja.refresh_from_db()
        self.assertEqual(loja.imagem_perfil.name, '')
        self.assertFalse(loja.imagem_perfil)

    def test_upload_to_gera_nome_aleatorio_em_minusculas_sem_nome_original(self):
        campo = Loja._meta.get_field('imagem_perfil')
        caminho = campo.upload_to(self.montar_loja(), 'Minha Foto.PNG')
        self.assertRegex(caminho, r'^lojas/[0-9a-f]{32}\.png$')
        self.assertNotIn('Minha', caminho)

    def test_extensoes_aceitas_passam_no_full_clean(self):
        for extensao in ['jpg', 'jpeg', 'png', 'webp', 'JPG']:
            with self.subTest(extensao=extensao):
                self.montar_loja(f'lojas/abc.{extensao}').full_clean()

    def test_extensao_nao_permitida_e_recusada_no_full_clean(self):
        for nome in ['lojas/abc.gif', 'lojas/abc.svg', 'lojas/abc.exe', 'lojas/abc']:
            with self.subTest(nome=nome):
                with self.assertRaises(ValidationError) as ctx:
                    self.montar_loja(nome).full_clean()
                self.assertIn('imagem_perfil', ctx.exception.message_dict)

    def test_valor_legado_e_preservado_ao_salvar_e_recarregar(self):
        loja = self.montar_loja('lojas/perfil/marcus.jpg')
        loja.save()
        loja.refresh_from_db()
        self.assertEqual(loja.imagem_perfil.name, 'lojas/perfil/marcus.jpg')

    def test_campo_tem_max_length_255_e_aceita_vazio(self):
        campo = Loja._meta.get_field('imagem_perfil')
        self.assertEqual(campo.max_length, 255)
        self.assertTrue(campo.blank)


MEDIA_ROOT_TESTES_LOJA = tempfile.mkdtemp()
PNG_VALIDO_LOJA = b'\x89PNG\r\n\x1a\n' + b'\x00' * 32
JPEG_VALIDO_LOJA = b'\xff\xd8\xff\xe0' + b'\x00' * 32
URL_MINHA_LOJA = '/api/v1/lojas/me/'
URL_IMAGEM_MINHA_LOJA = '/api/v1/lojas/me/imagem/'
MENSAGEM_IMAGEM_INVALIDA = 'Envie uma imagem JPG, PNG ou WEBP válida.'
MENSAGEM_IMAGEM_GRANDE = 'A imagem deve ter no máximo 5 MB.'
PADRAO_NOME_IMAGEM_LOJA = r'^lojas/[0-9a-f]{32}\.(jpg|jpeg|png|webp)$'


def criar_produtor(cpf, email, nome='Produtor Imagem'):
    genero, _ = Genero.objects.get_or_create(id_genero='M', defaults={'genero': 'Masculino'})
    return Usuario.objects.create_user(
        cpf=cpf, email=email, password='senha123', nome=nome,
        data_nascimento='1980-01-01', genero=genero, is_produtor=True,
    )


class LojaEdicaoPorIdBloqueadaTests(APITestCase):
    """BE-024: a loja só é editada pelo dono em /lojas/me/; a rota por id não aceita PATCH, PUT nem DELETE."""

    def setUp(self):
        self.dono = criar_produtor('98765432144', 'loja-dono@example.com')
        self.outro_produtor = criar_produtor('98765432155', 'loja-outro@example.com')
        self.loja = Loja.objects.create(proprietario=self.dono, nome='Feira do Dono', cnpj='98765432000144')
        self.url_loja = f'/api/v1/lojas/lojas/{self.loja.loja_id}/'

    def test_outro_produtor_recebe_405_em_patch_put_e_delete(self):
        self.client.force_authenticate(self.outro_produtor)
        respostas = [
            self.client.patch(self.url_loja, {'nome': 'Invadida'}, format='json'),
            self.client.put(self.url_loja, {'nome': 'Invadida', 'cnpj': '98765432000144'}, format='json'),
            self.client.delete(self.url_loja),
        ]

        for response in respostas:
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.loja.refresh_from_db()
        self.assertEqual(self.loja.nome, 'Feira do Dono')

    def test_dono_tambem_recebe_405_na_rota_por_id(self):
        self.client.force_authenticate(self.dono)

        response = self.client.patch(self.url_loja, {'nome': 'Outro nome'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.loja.refresh_from_db()
        self.assertEqual(self.loja.nome, 'Feira do Dono')


class ImagemLojaTestMixin:
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT_TESTES_LOJA, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        shutil.rmtree(MEDIA_ROOT_TESTES_LOJA, ignore_errors=True)
        os.makedirs(MEDIA_ROOT_TESTES_LOJA, exist_ok=True)
        self.produtor = criar_produtor('98765432166', 'loja-imagem@example.com')
        self.client.force_authenticate(self.produtor)

    def arquivo(self, nome='fachada.png', conteudo=PNG_VALIDO_LOJA):
        return SimpleUploadedFile(nome, conteudo, content_type='image/png')

    def arquivos_gravados(self):
        return sorted(
            os.path.relpath(os.path.join(pasta, nome), MEDIA_ROOT_TESTES_LOJA).replace(os.sep, '/')
            for pasta, _, nomes in os.walk(MEDIA_ROOT_TESTES_LOJA) for nome in nomes
        )

    def gravar_arquivo(self, nome, conteudo=PNG_VALIDO_LOJA):
        caminho = os.path.join(MEDIA_ROOT_TESTES_LOJA, *nome.split('/'))
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, 'wb') as arquivo:
            arquivo.write(conteudo)


@override_settings(MEDIA_ROOT=MEDIA_ROOT_TESTES_LOJA)
class LojaImagemPerfilAPITests(ImagemLojaTestMixin, APITestCase):
    def setUp(self):
        super().setUp()
        self.loja = Loja.objects.create(proprietario=self.produtor, nome='Feira Imagem', cnpj='98765432000166')

    def enviar(self, dados, format='multipart'):
        with self.captureOnCommitCallbacks(execute=True):
            return self.client.patch(URL_MINHA_LOJA, dados, format=format)

    def enviar_imagem_valida(self, nome='fachada.png', conteudo=PNG_VALIDO_LOJA):
        response = self.enviar({'imagem_perfil': self.arquivo(nome, conteudo)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.loja.refresh_from_db()
        return response

    def test_dono_envia_imagem_valida_com_nome_aleatorio_e_url_absoluta(self):
        response = self.enviar_imagem_valida()

        nome = self.loja.imagem_perfil.name
        self.assertRegex(nome, PADRAO_NOME_IMAGEM_LOJA)
        self.assertNotIn('fachada', nome)
        self.assertEqual(response.data['imagem_perfil'], f'http://testserver/media/{nome}')
        self.assertEqual(self.arquivos_gravados(), [nome])

        response = self.client.get(URL_MINHA_LOJA)
        self.assertEqual(response.data['imagem_perfil'], f'http://testserver/media/{nome}')

    def test_aceita_jpeg_e_webp(self):
        webp = b'RIFF\x00\x00\x00\x00WEBP' + b'\x00' * 16
        for nome, conteudo in (('foto.jpg', JPEG_VALIDO_LOJA), ('foto.webp', webp)):
            with self.subTest(nome=nome):
                self.enviar_imagem_valida(nome, conteudo)
                self.assertRegex(self.loja.imagem_perfil.name, PADRAO_NOME_IMAGEM_LOJA)

    def test_troca_substitui_e_apaga_arquivo_anterior_apos_commit(self):
        self.enviar_imagem_valida()
        nome_anterior = self.loja.imagem_perfil.name

        self.enviar_imagem_valida('nova.jpg', JPEG_VALIDO_LOJA)

        self.assertNotEqual(self.loja.imagem_perfil.name, nome_anterior)
        self.assertEqual(self.arquivos_gravados(), [self.loja.imagem_perfil.name])

    def test_recusas_mantem_imagem_atual_sem_apagar_nada(self):
        self.enviar_imagem_valida()
        nome_atual = self.loja.imagem_perfil.name
        grande = PNG_VALIDO_LOJA + b'\x00' * (5 * 1024 * 1024)
        envios = [
            ({'imagem_perfil': self.arquivo('fachada.png', grande)}, 'multipart', MENSAGEM_IMAGEM_GRANDE),
            ({'imagem_perfil': self.arquivo('fachada.gif')}, 'multipart', MENSAGEM_IMAGEM_INVALIDA),
            ({'imagem_perfil': self.arquivo('fachada.svg')}, 'multipart', MENSAGEM_IMAGEM_INVALIDA),
            ({'imagem_perfil': self.arquivo('fachada')}, 'multipart', MENSAGEM_IMAGEM_INVALIDA),
            ({'imagem_perfil': self.arquivo('fachada.png', b'nao sou uma imagem')}, 'multipart', MENSAGEM_IMAGEM_INVALIDA),
            ({'imagem_perfil': self.arquivo('fachada.png', b'')}, 'multipart', MENSAGEM_IMAGEM_INVALIDA),
            ({'imagem_perfil': ''}, 'multipart', MENSAGEM_IMAGEM_INVALIDA),
            ({'imagem_perfil': None}, 'json', MENSAGEM_IMAGEM_INVALIDA),
            ({'imagem_perfil': 'lojas/outra.png'}, 'json', MENSAGEM_IMAGEM_INVALIDA),
        ]

        for dados, formato, mensagem in envios:
            with self.subTest(dados=dados, formato=formato):
                response = self.enviar(dados, format=formato)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(response.data['imagem_perfil'], [mensagem])
                self.loja.refresh_from_db()
                self.assertEqual(self.loja.imagem_perfil.name, nome_atual)
                self.assertEqual(self.arquivos_gravados(), [nome_atual])

    def test_patch_so_com_imagem_em_loja_inativa_mantem_ativa_false(self):
        Loja.objects.filter(pk=self.loja.pk).update(ativa=False)

        response = self.enviar_imagem_valida()

        self.assertFalse(response.data['ativa'])
        self.assertFalse(self.loja.ativa)
        self.assertRegex(self.loja.imagem_perfil.name, PADRAO_NOME_IMAGEM_LOJA)

    def test_cnpj_e_proprietario_continuam_recusados(self):
        outro = criar_produtor('98765432177', 'loja-imagem-outro@example.com')
        for dados in ({'cnpj': '98765432000177'}, {'proprietario': outro.pk}):
            with self.subTest(dados=dados):
                response = self.enviar({**dados, 'imagem_perfil': self.arquivo()})
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(
                    response.data['detail'], 'Somente nome, descrição, imagem e status da loja podem ser alterados nesta área.',
                )

        self.loja.refresh_from_db()
        self.assertEqual(self.loja.cnpj, '98765432000166')
        self.assertEqual(self.loja.proprietario, self.produtor)
        self.assertEqual(self.loja.imagem_perfil.name, '')
        self.assertEqual(self.arquivos_gravados(), [])

    def test_delete_limpa_campo_e_arquivo(self):
        self.enviar_imagem_valida()

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.delete(URL_IMAGEM_MINHA_LOJA)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.loja.refresh_from_db()
        self.assertEqual(self.loja.imagem_perfil.name, '')
        self.assertEqual(self.arquivos_gravados(), [])
        self.assertIsNone(self.client.get(URL_MINHA_LOJA).data['imagem_perfil'])

    def test_delete_sem_imagem_retorna_404(self):
        response = self.client.delete(URL_IMAGEM_MINHA_LOJA)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'A loja não possui imagem.')

    def test_delete_sem_loja_retorna_404(self):
        self.client.force_authenticate(criar_produtor('98765432188', 'sem-loja-imagem@example.com'))

        response = self.client.delete(URL_IMAGEM_MINHA_LOJA)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Você não possui uma loja cadastrada.')

    def test_valor_legado_sai_como_null_e_delete_retorna_404_preservando_o_dado(self):
        Loja.objects.filter(pk=self.loja.pk).update(imagem_perfil='lojas/perfil/legado.jpg')

        self.assertIsNone(self.client.get(URL_MINHA_LOJA).data['imagem_perfil'])
        self.assertIsNone(self.client.get(f'/api/v1/lojas/lojas/{self.loja.loja_id}/').data['imagem_perfil'])
        response = self.client.delete(URL_IMAGEM_MINHA_LOJA)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.loja.refresh_from_db()
        self.assertEqual(self.loja.imagem_perfil.name, 'lojas/perfil/legado.jpg')

    def test_troca_de_valor_legado_compartilhado_nao_apaga_nada(self):
        self.gravar_arquivo('lojas/perfil/legado.jpg', JPEG_VALIDO_LOJA)
        outra = Loja.objects.create(
            proprietario=criar_produtor('98765432199', 'loja-legado@example.com'), nome='Outra Feira',
            cnpj='98765432000199', imagem_perfil='lojas/perfil/legado.jpg',
        )
        Loja.objects.filter(pk=self.loja.pk).update(imagem_perfil='lojas/perfil/legado.jpg')

        self.enviar_imagem_valida()

        outra.refresh_from_db()
        self.assertEqual(outra.imagem_perfil.name, 'lojas/perfil/legado.jpg')
        self.assertIn('lojas/perfil/legado.jpg', self.arquivos_gravados())

    def test_troca_nao_apaga_arquivo_gerenciado_usado_por_outra_loja(self):
        nome_compartilhado = 'lojas/' + 'a' * 32 + '.png'
        self.gravar_arquivo(nome_compartilhado)
        outra = Loja.objects.create(
            proprietario=criar_produtor('98765432199', 'loja-compartilhada@example.com'), nome='Outra Feira',
            cnpj='98765432000199', imagem_perfil=nome_compartilhado,
        )
        Loja.objects.filter(pk=self.loja.pk).update(imagem_perfil=nome_compartilhado)

        self.enviar_imagem_valida()

        outra.refresh_from_db()
        self.assertEqual(outra.imagem_perfil.name, nome_compartilhado)
        self.assertIn(nome_compartilhado, self.arquivos_gravados())

    def test_get_publico_retorna_url_absoluta(self):
        self.enviar_imagem_valida()
        self.client.force_authenticate(user=None)

        detalhe = self.client.get(f'/api/v1/lojas/lojas/{self.loja.loja_id}/')
        listagem = self.client.get('/api/v1/lojas/lojas/')

        url = f'http://testserver/media/{self.loja.imagem_perfil.name}'
        self.assertEqual(detalhe.data['imagem_perfil'], url)
        self.assertIn(url, [loja['imagem_perfil'] for loja in listagem.data])

    def test_sem_jwt_retorna_401(self):
        self.client.force_authenticate(user=None)

        patch = self.client.patch(URL_MINHA_LOJA, {'imagem_perfil': self.arquivo()}, format='multipart')
        delete = self.client.delete(URL_IMAGEM_MINHA_LOJA)

        self.assertEqual(patch.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.arquivos_gravados(), [])

    def test_falha_no_storage_registra_log_sem_dados_pessoais_e_nao_quebra_resposta(self):
        self.enviar_imagem_valida()
        nome_anterior = self.loja.imagem_perfil.name

        for erro in (OSError('disco'), ClientError({'Error': {'Code': '500'}}, 'DeleteObject')):
            with self.subTest(erro=type(erro).__name__):
                with mock.patch.object(FileSystemStorage, 'delete', side_effect=erro):
                    with self.assertLogs('agrostore.main.imagens', level='WARNING') as logs:
                        response = self.enviar({'imagem_perfil': self.arquivo()})

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                saida = '\n'.join(logs.output)
                for dado in (nome_anterior, self.produtor.email, self.produtor.cpf, self.produtor.nome):
                    self.assertNotIn(dado, saida)
                self.loja.refresh_from_db()
                nome_anterior = self.loja.imagem_perfil.name


@override_settings(MEDIA_ROOT=MEDIA_ROOT_TESTES_LOJA)
class LojaCriacaoComImagemAPITests(ImagemLojaTestMixin, APITestCase):
    def test_criacao_multipart_com_imagem_e_sem_ativa_cria_loja_ativa(self):
        response = self.client.post(
            '/api/v1/lojas/lojas/',
            {'nome': 'Feira Nova', 'cnpj': '98765432000133', 'imagem_perfil': self.arquivo()},
            format='multipart',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        loja = Loja.objects.get(cnpj='98765432000133')
        self.assertTrue(loja.ativa)
        self.assertRegex(loja.imagem_perfil.name, PADRAO_NOME_IMAGEM_LOJA)
        self.assertEqual(response.data['imagem_perfil'], f'http://testserver/media/{loja.imagem_perfil.name}')
        self.assertEqual(self.arquivos_gravados(), [loja.imagem_perfil.name])

    def test_criacao_com_imagem_invalida_nao_cria_loja(self):
        for arquivo in (self.arquivo('fachada.png', b'nao sou uma imagem'), self.arquivo('fachada.gif')):
            with self.subTest(arquivo=arquivo.name):
                response = self.client.post(
                    '/api/v1/lojas/lojas/',
                    {'nome': 'Feira Nova', 'cnpj': '98765432000133', 'imagem_perfil': arquivo},
                    format='multipart',
                )

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(response.data['imagem_perfil'], [MENSAGEM_IMAGEM_INVALIDA])
                self.assertFalse(Loja.objects.filter(cnpj='98765432000133').exists())
                self.assertEqual(self.arquivos_gravados(), [])

    def test_criacao_json_sem_imagem_retorna_null(self):
        response = self.client.post('/api/v1/lojas/lojas/', {'nome': 'Feira Nova', 'cnpj': '98765432000133'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data['imagem_perfil'])
        self.assertTrue(response.data['ativa'])


@override_settings(MEDIA_ROOT=MEDIA_ROOT_TESTES_LOJA)
class LojaImagemQaComplementaresTests(ImagemLojaTestMixin, APITestCase):
    """QA RN-018: isolamento entre proprietários, loja inativa e ausência da imagem no snapshot do pedido."""

    def setUp(self):
        super().setUp()
        self.loja = Loja.objects.create(proprietario=self.produtor, nome='Feira Imagem', cnpj='98765432000166')
        self.outro = criar_produtor('98765432200', 'loja-qa-outro@example.com')

    def gravar_imagem_do_dono(self):
        nome = 'lojas/' + 'b' * 32 + '.png'
        self.gravar_arquivo(nome)
        Loja.objects.filter(pk=self.loja.pk).update(imagem_perfil=nome)
        return nome

    def test_outro_produtor_nao_troca_nem_remove_imagem_da_loja_alheia(self):
        nome = self.gravar_imagem_do_dono()
        Loja.objects.create(proprietario=self.outro, nome='Outra', cnpj='98765432000200')
        self.client.force_authenticate(self.outro)

        with self.captureOnCommitCallbacks(execute=True):
            delete = self.client.delete(URL_IMAGEM_MINHA_LOJA)
            patch = self.client.patch(URL_MINHA_LOJA, {'imagem_perfil': self.arquivo()}, format='multipart')

        # DELETE nao tem alvo (a loja dele nao tem imagem); PATCH atua so na loja dele.
        self.assertEqual(delete.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        self.loja.refresh_from_db()
        self.assertEqual(self.loja.imagem_perfil.name, nome)
        self.assertIn(nome, self.arquivos_gravados())

    def test_usuario_sem_loja_nao_envia_imagem(self):
        self.client.force_authenticate(self.outro)

        response = self.client.patch(URL_MINHA_LOJA, {'imagem_perfil': self.arquivo()}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.arquivos_gravados(), [])

    def test_loja_inativa_aceita_remocao_da_imagem_pelo_dono_e_continua_inativa(self):
        self.gravar_imagem_do_dono()
        Loja.objects.filter(pk=self.loja.pk).update(ativa=False)

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.delete(URL_IMAGEM_MINHA_LOJA)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.loja.refresh_from_db()
        self.assertFalse(self.loja.ativa)
        self.assertEqual(self.loja.imagem_perfil.name, '')
        self.assertEqual(self.arquivos_gravados(), [])

    def test_desativar_a_loja_nao_apaga_a_imagem(self):
        nome = self.gravar_imagem_do_dono()

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.patch(URL_MINHA_LOJA, {'ativa': False}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.loja.refresh_from_db()
        self.assertFalse(self.loja.ativa)
        self.assertEqual(self.loja.imagem_perfil.name, nome)
        self.assertEqual(self.arquivos_gravados(), [nome])

    def test_snapshot_do_pedido_nao_guarda_imagem_da_loja_nem_foto_do_usuario(self):
        from agrostore.pedidos.models import Pedido, PedidoCliente, PedidoProduto

        nomes = {campo.name for modelo in (Pedido, PedidoProduto, PedidoCliente) for campo in modelo._meta.get_fields()}
        self.assertFalse([n for n in nomes if 'imagem' in n or 'foto' in n], nomes)


class LojaUnicaPorProdutorTests(APITestCase):
    """RN-013: uma loja por produtor, garantida na API e no banco; produtor com loja não é excluído."""

    MENSAGEM_LOJA_UNICA = 'Cada produtor pode possuir somente uma loja.'

    def setUp(self):
        self.genero, _ = Genero.objects.get_or_create(id_genero='M', defaults={'genero': 'Masculino'})
        self.produtor = self.criar_usuario('98765432201', 'unica-produtor@example.com', is_produtor=True)

    def criar_usuario(self, cpf, email, is_produtor=False, **extra):
        return Usuario.objects.create_user(
            cpf=cpf, email=email, password='senha123', nome='Usuário Teste',
            data_nascimento='1980-01-01', genero=self.genero, is_produtor=is_produtor, **extra,
        )

    def test_banco_recusa_segunda_loja_do_mesmo_proprietario(self):
        Loja.objects.create(proprietario=self.produtor, nome='Primeira', cnpj='98765432000201')

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Loja.objects.create(proprietario=self.produtor, nome='Segunda', cnpj='98765432000202')

        self.assertEqual(Loja.objects.filter(proprietario=self.produtor).count(), 1)

    def test_api_recusa_segunda_loja_com_mensagem_clara(self):
        self.client.force_authenticate(self.produtor)
        Loja.objects.create(proprietario=self.produtor, nome='Primeira', cnpj='98765432000201')

        response = self.client.post('/api/v1/lojas/lojas/', {'nome': 'Segunda', 'cnpj': '98765432000202'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': [self.MENSAGEM_LOJA_UNICA]})
        self.assertEqual(Loja.objects.filter(proprietario=self.produtor).count(), 1)

    def test_corrida_validate_passou_e_banco_recusou_responde_400_com_a_mesma_mensagem(self):
        self.client.force_authenticate(self.produtor)
        Loja.objects.create(proprietario=self.produtor, nome='Primeira', cnpj='98765432000201')

        with mock.patch.object(LojaSerializer, 'validate', new=lambda serializer, data: data):
            response = self.client.post('/api/v1/lojas/lojas/', {'nome': 'Segunda', 'cnpj': '98765432000202'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': [self.MENSAGEM_LOJA_UNICA]})
        self.assertEqual(Loja.objects.filter(proprietario=self.produtor).count(), 1)

    def test_corrida_com_outro_erro_de_unicidade_e_relancado_sem_a_mensagem_de_loja_unica(self):
        self.client.force_authenticate(self.produtor)

        with mock.patch.object(LojaSerializer, 'save', side_effect=IntegrityError('cnpj duplicado')):
            with self.assertRaises(IntegrityError):
                self.client.post('/api/v1/lojas/lojas/', {'nome': 'Sem Loja', 'cnpj': '98765432000203'}, format='json')

        self.assertFalse(Loja.objects.filter(proprietario=self.produtor).exists())

    def test_produtores_diferentes_podem_ter_cada_um_a_sua_loja(self):
        outro = self.criar_usuario('98765432202', 'unica-outro@example.com', is_produtor=True)

        for usuario, cnpj in [(self.produtor, '98765432000204'), (outro, '98765432000205')]:
            self.client.force_authenticate(usuario)
            response = self.client.post('/api/v1/lojas/lojas/', {'nome': 'Loja', 'cnpj': cnpj}, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Loja.objects.filter(proprietario=self.produtor).count(), 1)
        self.assertEqual(Loja.objects.filter(proprietario=outro).count(), 1)

    def test_excluir_produtor_com_loja_sem_pedidos_e_bloqueado(self):
        loja = Loja.objects.create(proprietario=self.produtor, nome='Primeira', cnpj='98765432000201')

        with self.assertRaises(ProtectedError):
            with transaction.atomic():
                self.produtor.delete()

        self.assertTrue(Usuario.objects.filter(pk=self.produtor.pk).exists())
        self.assertTrue(Loja.objects.filter(pk=loja.pk).exists())

    def test_admin_exclusao_de_produtor_com_loja_nao_da_erro_500_e_preserva_usuario_e_loja(self):
        loja = Loja.objects.create(proprietario=self.produtor, nome='Primeira', cnpj='98765432000201')
        admin = self.criar_usuario('98765432203', 'unica-admin@example.com', is_staff=True, is_superuser=True)
        self.client.force_login(admin)

        response = self.client.post(reverse('admin:usuarios_usuario_delete', args=[self.produtor.pk]), {'post': 'yes'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'protegid')
        self.assertTrue(Usuario.objects.filter(pk=self.produtor.pk).exists())
        self.assertTrue(Loja.objects.filter(pk=loja.pk).exists())

    def test_cliente_sem_loja_e_sem_pedidos_pode_ser_excluido(self):
        cliente = self.criar_usuario('98765432204', 'unica-cliente@example.com')

        cliente.delete()

        self.assertFalse(Usuario.objects.filter(pk=cliente.pk).exists())

    def test_api_nao_oferece_exclusao_de_loja_nem_de_usuario(self):
        loja = Loja.objects.create(proprietario=self.produtor, nome='Primeira', cnpj='98765432000201')
        self.client.force_authenticate(self.produtor)

        response = self.client.delete(f'/api/v1/lojas/lojas/{loja.loja_id}/')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(Loja.objects.filter(pk=loja.pk).exists())
