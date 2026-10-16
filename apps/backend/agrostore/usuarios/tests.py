import hashlib
import logging
import os
import re
import shutil
import smtplib
import tempfile
from datetime import date, timedelta
from decimal import Decimal
from unittest import mock

from botocore.exceptions import ClientError
from django.core import mail
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from agrostore.avaliacoes.models import Avaliacao
from agrostore.lojas.models import Loja
from agrostore.pedidos.models import Pedido, PedidoCliente, PedidoProduto, StatusPedido
from agrostore.produtos.models import Categoria, Produto
from . import redefinicao_senha
from .models import Genero, RedefinicaoSenha, Usuario


class CadastroClienteTests(APITestCase):
    url_cadastro = '/api/v1/usuarios/cadastro/'

    def setUp(self):
        self.genero, _ = Genero.objects.get_or_create(id_genero='M', defaults={'genero': 'Masculino'})
        self.dados_validos = {
            'nome': 'Cliente de Teste', 'cpf': '529.982.247-25', 'email': 'cliente@example.com',
            'telefone': '(51) 99999-0000', 'data_nascimento': '2000-05-10', 'genero': 'M',
            'password': 'SenhaForte123', 'password_confirmacao': 'SenhaForte123',
        }

    def criar_usuario(self, **campos):
        dados = {
            'cpf': '11144477735', 'email': 'existente@example.com', 'nome': 'Usuário Existente',
            'telefone': '51999990000', 'data_nascimento': date(2000, 1, 1), 'genero': self.genero,
            'password': 'SenhaForte123',
        }
        dados.update(campos)
        return Usuario.objects.create_user(**dados)

    def test_cadastra_cliente_normalizado_e_retorna_tokens(self):
        response = self.client.post(self.url_cadastro, self.dados_validos, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertNotIn('password', response.data['usuario'])
        usuario = Usuario.objects.get(cpf='52998224725')
        self.assertEqual(usuario.telefone, '51999990000')
        self.assertFalse(usuario.is_produtor)

    def test_rejeita_cpf_invalido(self):
        response = self.client.post(self.url_cadastro, {**self.dados_validos, 'cpf': '111.111.111-11'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cpf', response.data)

    def test_rejeita_cpf_e_email_duplicados(self):
        self.criar_usuario(cpf='52998224725')
        response = self.client.post(self.url_cadastro, self.dados_validos, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cpf', response.data)
        dados = {**self.dados_validos, 'cpf': '11144477735', 'email': 'existente@example.com'}
        response = self.client.post(self.url_cadastro, dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_rejeita_telefone_e_senha_invalidos(self):
        response = self.client.post(self.url_cadastro, {**self.dados_validos, 'telefone': '5199990000'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('telefone', response.data)
        dados = {**self.dados_validos, 'password': 'curta', 'password_confirmacao': 'curta'}
        response = self.client.post(self.url_cadastro, dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

        dados = {**self.dados_validos, 'password_confirmacao': 'OutraSenha123'}
        response = self.client.post(self.url_cadastro, dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password_confirmacao', response.data)

    def test_retorna_validacao_de_senha_comum_em_portugues(self):
        dados = {**self.dados_validos, 'password': 'password', 'password_confirmacao': 'password'}
        response = self.client.post(self.url_cadastro, dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password'][0], 'Esta senha é muito comum.')

    def test_rejeita_menor_de_16_anos_e_genero_invalido(self):
        nascimento = date.today() - timedelta(days=15 * 365)
        response = self.client.post(self.url_cadastro, {**self.dados_validos, 'data_nascimento': nascimento.isoformat()}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('data_nascimento', response.data)
        response = self.client.post(self.url_cadastro, {**self.dados_validos, 'genero': 'X'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('genero', response.data)

    def test_ignora_campos_de_privilegio_no_cadastro(self):
        dados = {**self.dados_validos, 'is_produtor': True, 'is_staff': True}
        response = self.client.post(self.url_cadastro, dados, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        usuario = Usuario.objects.get(cpf='52998224725')
        self.assertFalse(usuario.is_produtor)
        self.assertFalse(usuario.is_staff)

    def test_endpoint_generico_de_usuarios_nao_esta_exposto(self):
        response = self.client.get('/api/v1/usuarios/usuarios/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_endpoint_de_solicitacao_de_produtor_nao_esta_exposto(self):
        response = self.client.post('/api/v1/usuarios/me/solicitacao-produtor/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AtualizacaoPerfilTests(APITestCase):
    url_perfil = '/api/v1/usuarios/me/'

    def setUp(self):
        self.genero, _ = Genero.objects.get_or_create(id_genero='M', defaults={'genero': 'Masculino'})
        Genero.objects.get_or_create(id_genero='F', defaults={'genero': 'Feminino'})
        self.usuario = Usuario.objects.create_user(
            cpf='52998224725', email='perfil@example.com', password='SenhaForte123', nome='Cliente Perfil',
            telefone='51999990000', data_nascimento=date(2000, 1, 1), genero=self.genero,
        )
        self.client.force_authenticate(self.usuario)

    def test_atualiza_dados_pessoais_normalizados(self):
        dados = {
            'nome': 'Cliente Atualizado', 'email': 'NOVO@Example.com', 'telefone': '(51) 98888-7777',
            'data_nascimento': '1995-03-20', 'genero': 'F',
        }
        response = self.client.patch(self.url_perfil, dados, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Cliente Atualizado')
        self.assertEqual(response.data['genero'], 'F')
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.email, 'novo@example.com')
        self.assertEqual(self.usuario.telefone, '51988887777')

    def test_mantem_o_proprio_email_sem_acusar_duplicidade(self):
        response = self.client.patch(self.url_perfil, {'email': 'perfil@example.com', 'nome': 'Outro Nome'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rejeita_cpf_e_campos_de_privilegio(self):
        for campo, valor in (('cpf', '11144477735'), ('is_produtor', True), ('is_staff', True)):
            response = self.client.patch(self.url_perfil, {campo: valor}, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.cpf, '52998224725')
        self.assertFalse(self.usuario.is_produtor)
        self.assertFalse(self.usuario.is_staff)

    def test_rejeita_email_de_outro_usuario_e_menor_de_16_anos(self):
        Usuario.objects.create_user(
            cpf='11144477735', email='outro@example.com', password='SenhaForte123', nome='Outro',
            data_nascimento=date(2000, 1, 1), genero=self.genero,
        )
        response = self.client.patch(self.url_perfil, {'email': 'OUTRO@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], 'Já existe uma conta cadastrada com este e-mail.')

        nascimento = date.today() - timedelta(days=15 * 365)
        response = self.client.patch(self.url_perfil, {'data_nascimento': nascimento.isoformat()}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('data_nascimento', response.data)

    def test_exige_autenticacao(self):
        self.client.force_authenticate(user=None)
        response = self.client.patch(self.url_perfil, {'nome': 'Sem login'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UsuarioFotoPerfilModelTests(TestCase):
    def setUp(self):
        self.genero, _ = Genero.objects.get_or_create(id_genero='M', defaults={'genero': 'Masculino'})

    def montar_usuario(self, foto=''):
        usuario = Usuario(
            cpf='11122233344', email='foto-model@example.com', nome='Usuario Foto',
            data_nascimento='1990-01-01', genero=self.genero,
        )
        if foto:
            usuario.foto_perfil.name = foto
        return usuario

    def test_usuario_novo_nasce_sem_foto_com_texto_vazio(self):
        usuario = Usuario.objects.create_user(
            cpf='11122233355', email='sem-foto@example.com', password='senha12345',
            nome='Sem Foto', data_nascimento='1990-01-01', genero=self.genero,
        )
        usuario.refresh_from_db()
        self.assertEqual(usuario.foto_perfil.name, '')
        self.assertFalse(usuario.foto_perfil)

    def test_campo_foto_perfil_nao_aceita_null_e_tem_max_length_255(self):
        campo = Usuario._meta.get_field('foto_perfil')
        self.assertFalse(campo.null)
        self.assertTrue(campo.blank)
        self.assertEqual(campo.max_length, 255)

    def test_upload_to_gera_nome_aleatorio_em_minusculas_sem_nome_original(self):
        campo = Usuario._meta.get_field('foto_perfil')
        caminho = campo.upload_to(self.montar_usuario(), 'Minha Foto.WEBP')
        self.assertRegex(caminho, r'^usuarios/[0-9a-f]{32}\.webp$')
        self.assertNotIn('Minha', caminho)

    def test_extensoes_aceitas_passam_no_full_clean(self):
        for extensao in ['jpg', 'jpeg', 'png', 'webp', 'PNG']:
            with self.subTest(extensao=extensao):
                usuario = self.montar_usuario(f'usuarios/abc.{extensao}')
                usuario.full_clean(exclude=['password'])

    def test_extensao_nao_permitida_e_recusada_no_full_clean(self):
        for nome in ['usuarios/abc.gif', 'usuarios/abc.svg', 'usuarios/abc.pdf', 'usuarios/abc']:
            with self.subTest(nome=nome):
                with self.assertRaises(ValidationError) as ctx:
                    self.montar_usuario(nome).full_clean(exclude=['password'])
                self.assertIn('foto_perfil', ctx.exception.message_dict)


MEDIA_ROOT_TESTES_USUARIO = tempfile.mkdtemp()
PNG_VALIDO_USUARIO = b'\x89PNG\r\n\x1a\n' + b'\x00' * 32
JPEG_VALIDO_USUARIO = b'\xff\xd8\xff\xe0' + b'\x00' * 32
MENSAGEM_IMAGEM_INVALIDA = 'Envie uma imagem JPG, PNG ou WEBP válida.'
MENSAGEM_IMAGEM_GRANDE = 'A imagem deve ter no máximo 5 MB.'
PADRAO_NOME_FOTO = r'^usuarios/[0-9a-f]{32}\.(jpg|jpeg|png|webp)$'
FOTO_GERENCIADA = 'usuarios/' + 'b' * 32 + '.png'


@override_settings(MEDIA_ROOT=MEDIA_ROOT_TESTES_USUARIO)
class FotoPerfilAPITests(APITestCase):
    url_perfil = '/api/v1/usuarios/me/'
    url_foto = '/api/v1/usuarios/me/foto/'

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT_TESTES_USUARIO, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        shutil.rmtree(MEDIA_ROOT_TESTES_USUARIO, ignore_errors=True)
        os.makedirs(MEDIA_ROOT_TESTES_USUARIO, exist_ok=True)
        self.genero, _ = Genero.objects.get_or_create(id_genero='M', defaults={'genero': 'Masculino'})
        self.usuario = Usuario.objects.create_user(
            cpf='52998224725', email='foto@example.com', password='SenhaForte123', nome='Cliente Foto',
            telefone='51999990000', data_nascimento=date(2000, 1, 1), genero=self.genero,
        )
        self.client.force_authenticate(self.usuario)

    def arquivo(self, nome='rosto.png', conteudo=PNG_VALIDO_USUARIO):
        return SimpleUploadedFile(nome, conteudo, content_type='image/png')

    def arquivos_gravados(self):
        return sorted(
            os.path.relpath(os.path.join(pasta, nome), MEDIA_ROOT_TESTES_USUARIO).replace(os.sep, '/')
            for pasta, _, nomes in os.walk(MEDIA_ROOT_TESTES_USUARIO) for nome in nomes
        )

    def enviar(self, dados, format='multipart'):
        with self.captureOnCommitCallbacks(execute=True):
            return self.client.patch(self.url_perfil, dados, format=format)

    def enviar_foto_valida(self, nome='rosto.png', conteudo=PNG_VALIDO_USUARIO):
        response = self.enviar({'foto_perfil': self.arquivo(nome, conteudo)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.usuario.refresh_from_db()
        return response

    def test_envia_foto_valida_com_nome_aleatorio_e_url_absoluta(self):
        response = self.enviar_foto_valida()

        nome = self.usuario.foto_perfil.name
        self.assertRegex(nome, PADRAO_NOME_FOTO)
        self.assertNotIn('rosto', nome)
        self.assertEqual(response.data['foto_perfil'], f'http://testserver/media/{nome}')
        self.assertEqual(self.arquivos_gravados(), [nome])
        self.assertEqual(self.client.get(self.url_perfil).data['foto_perfil'], f'http://testserver/media/{nome}')

    def test_multipart_altera_dados_e_foto_juntos(self):
        response = self.enviar({'nome': 'Nome Novo', 'foto_perfil': self.arquivo()})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.nome, 'Nome Novo')
        self.assertRegex(self.usuario.foto_perfil.name, PADRAO_NOME_FOTO)

    def test_troca_substitui_e_apaga_arquivo_anterior_apos_commit(self):
        self.enviar_foto_valida()
        nome_anterior = self.usuario.foto_perfil.name

        self.enviar_foto_valida('nova.jpg', JPEG_VALIDO_USUARIO)

        self.assertNotEqual(self.usuario.foto_perfil.name, nome_anterior)
        self.assertEqual(self.arquivos_gravados(), [self.usuario.foto_perfil.name])

    def test_recusas_mantem_foto_atual_sem_apagar_nada(self):
        self.enviar_foto_valida()
        nome_atual = self.usuario.foto_perfil.name
        grande = PNG_VALIDO_USUARIO + b'\x00' * (5 * 1024 * 1024)
        envios = [
            ({'foto_perfil': self.arquivo('rosto.png', grande)}, 'multipart', MENSAGEM_IMAGEM_GRANDE),
            ({'foto_perfil': self.arquivo('rosto.gif')}, 'multipart', MENSAGEM_IMAGEM_INVALIDA),
            ({'foto_perfil': self.arquivo('rosto')}, 'multipart', MENSAGEM_IMAGEM_INVALIDA),
            ({'foto_perfil': self.arquivo('rosto.png', b'nao sou uma imagem')}, 'multipart', MENSAGEM_IMAGEM_INVALIDA),
            ({'foto_perfil': ''}, 'multipart', MENSAGEM_IMAGEM_INVALIDA),
            ({'foto_perfil': None}, 'json', MENSAGEM_IMAGEM_INVALIDA),
        ]

        for dados, formato, mensagem in envios:
            with self.subTest(dados=dados, formato=formato):
                response = self.enviar(dados, format=formato)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(response.data['foto_perfil'], [mensagem])
                self.usuario.refresh_from_db()
                self.assertEqual(self.usuario.foto_perfil.name, nome_atual)
                self.assertEqual(self.arquivos_gravados(), [nome_atual])

    def test_cpf_e_campos_de_privilegio_continuam_recusados_com_foto(self):
        for campo, valor in (('cpf', '11144477735'), ('is_produtor', 'true'), ('is_staff', 'true')):
            with self.subTest(campo=campo):
                response = self.enviar({campo: valor, 'foto_perfil': self.arquivo()})
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(
                    response.data['detail'],
                    'Somente nome, e-mail, celular, data de nascimento, gênero e foto de perfil podem ser alterados no perfil.',
                )

        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.cpf, '52998224725')
        self.assertFalse(self.usuario.is_produtor)
        self.assertFalse(self.usuario.is_staff)
        self.assertEqual(self.usuario.foto_perfil.name, '')
        self.assertEqual(self.arquivos_gravados(), [])

    def test_delete_limpa_campo_e_arquivo(self):
        self.enviar_foto_valida()

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.delete(self.url_foto)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.foto_perfil.name, '')
        self.assertEqual(self.arquivos_gravados(), [])
        self.assertIsNone(self.client.get(self.url_perfil).data['foto_perfil'])

    def test_delete_sem_foto_retorna_404(self):
        response = self.client.delete(self.url_foto)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Você não possui foto de perfil.')

    def test_valor_fora_do_padrao_sai_como_null_e_delete_retorna_404_preservando_o_dado(self):
        Usuario.objects.filter(pk=self.usuario.pk).update(foto_perfil='usuarios/legado.jpg')

        self.assertIsNone(self.client.get(self.url_perfil).data['foto_perfil'])
        response = self.client.delete(self.url_foto)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.foto_perfil.name, 'usuarios/legado.jpg')

    def test_sem_jwt_retorna_401(self):
        self.client.force_authenticate(user=None)

        patch = self.client.patch(self.url_perfil, {'foto_perfil': self.arquivo()}, format='multipart')
        delete = self.client.delete(self.url_foto)

        self.assertEqual(patch.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.arquivos_gravados(), [])

    def test_falha_no_storage_registra_log_sem_dados_pessoais_e_nao_quebra_resposta(self):
        self.enviar_foto_valida()
        nome_anterior = self.usuario.foto_perfil.name

        for erro in (OSError('disco'), ClientError({'Error': {'Code': '500'}}, 'DeleteObject')):
            with self.subTest(erro=type(erro).__name__):
                with mock.patch.object(FileSystemStorage, 'delete', side_effect=erro):
                    with self.assertLogs('agrostore.main.imagens', level='WARNING') as logs:
                        response = self.enviar({'foto_perfil': self.arquivo()})

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                saida = '\n'.join(logs.output)
                for dado in (nome_anterior, self.usuario.email, self.usuario.cpf, self.usuario.nome):
                    self.assertNotIn(dado, saida)
                self.usuario.refresh_from_db()
                nome_anterior = self.usuario.foto_perfil.name

    def test_login_e_cadastro_retornam_foto_perfil(self):
        Usuario.objects.filter(pk=self.usuario.pk).update(foto_perfil=FOTO_GERENCIADA)
        self.client.force_authenticate(user=None)

        login = self.client.post('/api/v1/usuarios/login/', {'cpf': '52998224725', 'password': 'SenhaForte123'}, format='json')
        cadastro = self.client.post('/api/v1/usuarios/cadastro/', {
            'nome': 'Cliente Novo', 'cpf': '111.444.777-35', 'email': 'novo-foto@example.com',
            'telefone': '(51) 98888-0000', 'data_nascimento': '2000-05-10', 'genero': 'M',
            'password': 'SenhaForte123', 'password_confirmacao': 'SenhaForte123',
        }, format='json')

        self.assertEqual(login.status_code, status.HTTP_200_OK)
        self.assertEqual(login.data['usuario']['foto_perfil'], f'http://testserver/media/{FOTO_GERENCIADA}')
        self.assertEqual(cadastro.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(cadastro.data['usuario']['foto_perfil'])


class FotoPerfilNaoExpostaATerceirosTests(APITestCase):
    """RN-018: a foto do usuário é exibida só ao próprio usuário."""

    def setUp(self):
        genero, _ = Genero.objects.get_or_create(id_genero='M', defaults={'genero': 'Masculino'})
        self.cliente = Usuario.objects.create_user(
            cpf='52998224725', email='cliente-foto@example.com', password='SenhaForte123', nome='Cliente Foto',
            telefone='51999990000', data_nascimento=date(2000, 1, 1), genero=genero, foto_perfil=FOTO_GERENCIADA,
        )
        self.produtor = Usuario.objects.create_user(
            cpf='11144477735', email='produtor-foto@example.com', password='SenhaForte123', nome='Produtor Foto',
            data_nascimento=date(1980, 1, 1), genero=genero, is_produtor=True,
            foto_perfil='usuarios/' + 'c' * 32 + '.png',
        )
        self.loja = Loja.objects.create(proprietario=self.produtor, nome='Feira Foto', cnpj='11144477000135')
        self.produto = Produto.objects.create(
            loja=self.loja, nome='Alface', estoque=10, sku='ALF-001', categoria=Categoria.objects.create(nome='Verduras'),
        )
        pedido = Pedido.objects.create(loja=self.loja, status=StatusPedido.objects.create(status='Entregue'))
        PedidoCliente.objects.create(
            pedido=pedido, usuario=self.cliente, nome=self.cliente.nome, cpf=self.cliente.cpf, email=self.cliente.email,
            telefone=self.cliente.telefone, data_nascimento=self.cliente.data_nascimento, genero=str(genero),
        )
        item = PedidoProduto.objects.create(
            pedido=pedido, produto=self.produto, nome_produto=self.produto.nome, quantidade=1,
            valor_unitario=Decimal('5.00'), subtotal=Decimal('5.00'),
        )
        Avaliacao.objects.create(usuario=self.cliente, produto=self.produto, pedido_produto=item, nota=5)

    def assertSemFoto(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(b'foto_perfil', response.content)
        self.assertNotIn(b'b' * 32, response.content)
        self.assertNotIn(b'c' * 32, response.content)

    def test_foto_nao_aparece_nos_pedidos_do_produtor(self):
        self.client.force_authenticate(self.produtor)
        self.assertSemFoto(self.client.get('/api/v1/pedidos/minha-loja/'))

    def test_foto_nao_aparece_nos_pedidos_do_cliente(self):
        self.client.force_authenticate(self.cliente)
        self.assertSemFoto(self.client.get('/api/v1/pedidos/'))

    def test_foto_nao_aparece_nas_avaliacoes_publicas(self):
        self.assertSemFoto(self.client.get(f'/api/v1/avaliacoes/?produto={self.produto.produto_id}'))

    def test_foto_do_proprietario_nao_aparece_na_loja_publica(self):
        self.assertSemFoto(self.client.get(f'/api/v1/lojas/lojas/{self.loja.loja_id}/'))
        self.assertSemFoto(self.client.get('/api/v1/lojas/lojas/'))
        self.assertSemFoto(self.client.get(f'/api/v1/produtos/{self.produto.produto_id}/'))


MENSAGEM_SOLICITACAO = 'Se houver uma conta com este e-mail, enviaremos um link para redefinir a senha.'
MENSAGEM_LINK_INVALIDO = 'Este link de redefinição é inválido ou expirou. Solicite um novo.'
MENSAGEM_SUCESSO = 'Senha redefinida. Entre com a nova senha.'
MENSAGEM_LIMITE = 'Muitas solicitações. Tente novamente mais tarde.'


@override_settings(FRONTEND_URL='http://front.test')
class RedefinicaoSenhaBaseTests(APITestCase):
    url_solicitacao = '/api/v1/usuarios/redefinir-senha/'
    url_confirmacao = '/api/v1/usuarios/redefinir-senha/confirmar/'
    url_login = '/api/v1/usuarios/login/'
    senha_antiga = 'SenhaForte123'
    senha_nova = 'NovaSenhaSegura456'

    def setUp(self):
        cache.clear()
        self.genero, _ = Genero.objects.get_or_create(id_genero='M', defaults={'genero': 'Masculino'})
        self.usuario = self.criar_usuario()

    def criar_usuario(self, **campos):
        dados = {
            'cpf': '11144477735', 'email': 'cliente@example.com', 'nome': 'Cliente de Teste',
            'telefone': '51999990000', 'data_nascimento': date(2000, 1, 1), 'genero': self.genero,
            'password': self.senha_antiga,
        }
        dados.update(campos)
        return Usuario.objects.create_user(**dados)

    def criar_link(self, usuario=None):
        token = redefinicao_senha.gerar_token()
        RedefinicaoSenha.objects.create(
            usuario=usuario or self.usuario,
            token_hash=redefinicao_senha.calcular_hash(token),
            data_expiracao=timezone.now() + timedelta(minutes=30),
        )
        return token

    def expirar(self, token):
        """Cria-se o registro válido e depois ele é vencido por update, sem violar o CHECK do banco."""
        agora = timezone.now()
        RedefinicaoSenha.objects.filter(token_hash=redefinicao_senha.calcular_hash(token)).update(
            data_criacao=agora - timedelta(minutes=40), data_expiracao=agora - timedelta(minutes=10),
        )

    def solicitar(self, email, **extra):
        with self.captureOnCommitCallbacks(execute=True):
            return self.client.post(self.url_solicitacao, {'email': email}, format='json', **extra)

    def confirmar(self, token, senha=None, confirmacao=None, **extra):
        senha = senha or self.senha_nova
        dados = {'token': token, 'password': senha, 'password_confirmacao': confirmacao or senha}
        return self.client.post(self.url_confirmacao, dados, format='json', **extra)

    def token_do_email(self, indice=-1):
        return re.search(r'#token=([\w-]+)', mail.outbox[indice].body).group(1)

    def login(self, senha):
        return self.client.post(self.url_login, {'cpf': self.usuario.cpf, 'password': senha}, format='json')


class SolicitacaoRedefinicaoSenhaTests(RedefinicaoSenhaBaseTests):
    def test_email_existente_cria_link_e_envia_email(self):
        resposta = self.solicitar('cliente@example.com')

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data, {'detail': MENSAGEM_SOLICITACAO})
        self.assertEqual(RedefinicaoSenha.objects.filter(usuario=self.usuario).count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['cliente@example.com'])
        self.assertIn('http://front.test/redefinir-senha#token=', mail.outbox[0].body)

    def test_busca_email_sem_diferenciar_maiusculas(self):
        resposta = self.solicitar('CLIENTE@Example.COM')

        self.assertEqual(resposta.data, {'detail': MENSAGEM_SOLICITACAO})
        self.assertEqual(len(mail.outbox), 1)

    def test_email_inexistente_responde_igual_sem_enviar(self):
        resposta = self.solicitar('ninguem@example.com')

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data, {'detail': MENSAGEM_SOLICITACAO})
        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(RedefinicaoSenha.objects.exists())

    def test_conta_inativa_responde_igual_sem_enviar(self):
        self.usuario.is_active = False
        self.usuario.save(update_fields=['is_active'])

        resposta = self.solicitar('cliente@example.com')

        self.assertEqual(resposta.data, {'detail': MENSAGEM_SOLICITACAO})
        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(RedefinicaoSenha.objects.exists())

    def test_email_duplicado_por_maiusculas_nao_recebe_link(self):
        self.criar_usuario(cpf='52998224725', email='CLIENTE@example.com')

        with self.assertLogs('agrostore.usuarios.redefinicao_senha', level='WARNING') as logs:
            resposta = self.solicitar('cliente@example.com')

        self.assertNotIn('cliente@example.com', ' '.join(logs.output).lower())

        self.assertEqual(resposta.data, {'detail': MENSAGEM_SOLICITACAO})
        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(RedefinicaoSenha.objects.exists())

    def test_salva_somente_o_hash_do_token(self):
        self.solicitar('cliente@example.com')
        token = self.token_do_email()
        redefinicao = RedefinicaoSenha.objects.get()

        self.assertNotEqual(redefinicao.token_hash, token)
        self.assertEqual(redefinicao.token_hash, hashlib.sha256(token.encode()).hexdigest())
        self.assertFalse(RedefinicaoSenha.objects.filter(token_hash=token).exists())

    def test_link_vale_30_minutos_e_respeita_o_check_do_banco(self):
        self.solicitar('cliente@example.com')
        redefinicao = RedefinicaoSenha.objects.get()

        validade = redefinicao.data_expiracao - redefinicao.data_criacao
        self.assertGreater(redefinicao.data_expiracao, redefinicao.data_criacao)
        self.assertAlmostEqual(validade.total_seconds(), 30 * 60, delta=5)
        self.assertIsNone(redefinicao.data_utilizacao)

    def test_novo_pedido_invalida_links_pendentes(self):
        self.solicitar('cliente@example.com')
        token_antigo = self.token_do_email()
        self.solicitar('cliente@example.com')

        antigo = RedefinicaoSenha.objects.get(token_hash=redefinicao_senha.calcular_hash(token_antigo))
        self.assertIsNotNone(antigo.data_utilizacao)
        self.assertEqual(RedefinicaoSenha.objects.filter(data_utilizacao__isnull=True).count(), 1)
        resposta = self.confirmar(token_antigo)
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resposta.data, {'detail': MENSAGEM_LINK_INVALIDO})

    def test_email_ausente_ou_invalido_retorna_400(self):
        for corpo in [{}, {'email': 'nao-e-email'}]:
            with self.subTest(corpo=corpo):
                resposta = self.client.post(self.url_solicitacao, corpo, format='json')
                self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn('email', resposta.data)

    def test_falha_no_envio_mantem_resposta_neutra_e_nao_registra_dados_sensiveis(self):
        with mock.patch('agrostore.usuarios.redefinicao_senha.send_mail', side_effect=smtplib.SMTPException('falha')):
            with self.assertLogs('agrostore.usuarios.redefinicao_senha', level='ERROR') as logs:
                resposta = self.solicitar('cliente@example.com')

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data, {'detail': MENSAGEM_SOLICITACAO})
        token_hash = RedefinicaoSenha.objects.get().token_hash
        for linha in logs.output:
            self.assertNotIn('cliente@example.com', linha)
            self.assertNotIn(token_hash, linha)

    def test_jwt_invalido_no_header_nao_bloqueia(self):
        resposta = self.solicitar('cliente@example.com', HTTP_AUTHORIZATION='Bearer token-invalido')

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)


class ConfirmacaoRedefinicaoSenhaTests(RedefinicaoSenhaBaseTests):
    def test_troca_a_senha_sem_devolver_jwt(self):
        token = self.criar_link()

        resposta = self.confirmar(token)

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data, {'detail': MENSAGEM_SUCESSO})
        self.assertNotIn('access', resposta.data)
        self.assertNotIn('refresh', resposta.data)
        self.assertEqual(self.login(self.senha_nova).status_code, status.HTTP_200_OK)
        self.assertEqual(self.login(self.senha_antiga).status_code, status.HTTP_400_BAD_REQUEST)

    def test_link_e_de_uso_unico(self):
        token = self.criar_link()
        self.confirmar(token)

        redefinicao = RedefinicaoSenha.objects.get(token_hash=redefinicao_senha.calcular_hash(token))
        self.assertIsNotNone(redefinicao.data_utilizacao)
        resposta = self.confirmar(token, senha='OutraSenhaSegura789')
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resposta.data, {'detail': MENSAGEM_LINK_INVALIDO})
        self.assertEqual(self.login(self.senha_nova).status_code, status.HTTP_200_OK)

    def test_link_expirado_e_recusado(self):
        token = self.criar_link()
        self.expirar(token)

        resposta = self.confirmar(token)

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resposta.data, {'detail': MENSAGEM_LINK_INVALIDO})
        self.assertEqual(self.login(self.senha_antiga).status_code, status.HTTP_200_OK)

    def test_link_que_expira_entre_a_leitura_e_o_uso_e_recusado(self):
        token = self.criar_link()
        redefinicao = redefinicao_senha.buscar_redefinicao_valida(token)
        self.expirar(token)

        with self.assertRaises(redefinicao_senha.LinkRedefinicaoInvalido):
            redefinicao_senha.confirmar_redefinicao(redefinicao, self.senha_nova)

        redefinicao.refresh_from_db()
        self.assertIsNone(redefinicao.data_utilizacao)
        self.assertEqual(self.login(self.senha_antiga).status_code, status.HTTP_200_OK)

    def test_conta_desativada_entre_a_busca_e_a_confirmacao_desfaz_a_marcacao_do_link(self):
        token = self.criar_link()
        redefinicao = redefinicao_senha.buscar_redefinicao_valida(token)
        Usuario.objects.filter(pk=self.usuario.pk).update(is_active=False)

        with self.assertRaises(redefinicao_senha.LinkRedefinicaoInvalido):
            redefinicao_senha.confirmar_redefinicao(redefinicao, self.senha_nova)

        redefinicao.refresh_from_db()
        self.assertIsNone(redefinicao.data_utilizacao)
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.check_password(self.senha_antiga))
        self.assertFalse(self.usuario.check_password(self.senha_nova))

    def test_token_inexistente_e_recusado(self):
        resposta = self.confirmar(redefinicao_senha.gerar_token())

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resposta.data, {'detail': MENSAGEM_LINK_INVALIDO})

    def test_conta_inativa_recebe_mensagem_de_link_invalido(self):
        token = self.criar_link()
        self.usuario.is_active = False
        self.usuario.save(update_fields=['is_active'])

        resposta = self.confirmar(token)

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resposta.data, {'detail': MENSAGEM_LINK_INVALIDO})
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.check_password(self.senha_antiga))

    def test_senha_invalida_mantem_o_link_sem_uso(self):
        token = self.criar_link()
        casos = [
            ('Curta1', 'Curta1', 'password'),
            ('12345678', '12345678', 'password'),
            ('senha123', 'senha123', 'password'),
            (self.senha_nova, 'Diferente123', 'password_confirmacao'),
        ]
        for senha, confirmacao, campo in casos:
            with self.subTest(senha=senha, campo=campo):
                resposta = self.confirmar(token, senha=senha, confirmacao=confirmacao)
                self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(campo, resposta.data)

        redefinicao = RedefinicaoSenha.objects.get(token_hash=redefinicao_senha.calcular_hash(token))
        self.assertIsNone(redefinicao.data_utilizacao)
        self.assertEqual(self.confirmar(token).status_code, status.HTTP_200_OK)

    def test_troca_invalida_os_demais_links_pendentes(self):
        token_usado = self.criar_link()
        outro_token = self.criar_link()

        self.confirmar(token_usado)

        self.assertFalse(RedefinicaoSenha.objects.filter(usuario=self.usuario, data_utilizacao__isnull=True).exists())
        self.assertEqual(self.confirmar(outro_token).data, {'detail': MENSAGEM_LINK_INVALIDO})

    def test_jwt_invalido_no_header_nao_retorna_401(self):
        resposta = self.confirmar(redefinicao_senha.gerar_token(), HTTP_AUTHORIZATION='Bearer token-invalido')

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resposta.data, {'detail': MENSAGEM_LINK_INVALIDO})


class LimiteRedefinicaoSenhaTests(RedefinicaoSenhaBaseTests):
    def test_solicitacao_limitada_a_5_por_hora(self):
        for _ in range(5):
            self.assertEqual(self.solicitar('ninguem@example.com').status_code, status.HTTP_200_OK)

        resposta = self.solicitar('ninguem@example.com')

        self.assertEqual(resposta.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertEqual(resposta.data, {'detail': MENSAGEM_LIMITE})
        self.assertIn('Retry-After', resposta.headers)

    def test_confirmacao_limitada_a_10_por_hora(self):
        for _ in range(10):
            self.assertEqual(self.confirmar('token-invalido').status_code, status.HTTP_400_BAD_REQUEST)

        resposta = self.confirmar('token-invalido')

        self.assertEqual(resposta.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertEqual(resposta.data, {'detail': MENSAGEM_LIMITE})
        self.assertIn('Retry-After', resposta.headers)

    def test_x_forwarded_for_variado_nao_burla_o_limite(self):
        for indice in range(5):
            self.solicitar('ninguem@example.com', HTTP_X_FORWARDED_FOR=f'203.0.113.{indice}')

        resposta = self.solicitar('ninguem@example.com', HTTP_X_FORWARDED_FOR='198.51.100.99')

        self.assertEqual(resposta.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class QaRedefinicaoSenhaComplementaresTests(RedefinicaoSenhaBaseTests):
    """Casos de QA (SCRUM-125/SCRUM-124): segredos, isolamento de endpoints e integridade do modelo."""

    def test_resposta_da_solicitacao_e_do_log_nao_trazem_o_token(self):
        with self.assertLogs('agrostore', level='DEBUG') as logs:
            logging.getLogger('agrostore').debug('marcador')
            resposta = self.solicitar('cliente@example.com')
        token = self.token_do_email()

        self.assertNotIn(token, str(resposta.content))
        self.assertNotIn(token, ' '.join(logs.output))

    def test_email_traz_link_com_fragmento_e_nao_traz_senha(self):
        self.solicitar('cliente@example.com')
        corpo = mail.outbox[0].body

        self.assertIn('/redefinir-senha#token=', corpo)
        self.assertNotIn('?token=', corpo)
        self.assertNotIn(self.senha_antiga, corpo)
        self.assertNotIn(self.usuario.password, corpo)

    def test_resposta_da_confirmacao_nao_traz_token_nem_hash(self):
        token = self.criar_link()
        resposta = self.confirmar(token)

        self.assertNotIn(token, str(resposta.content))
        self.assertNotIn(redefinicao_senha.calcular_hash(token), str(resposta.content))

    def test_confirmacao_sem_jwt_nao_autentica_em_endpoint_protegido(self):
        token = self.criar_link()
        self.confirmar(token)

        resposta = self.client.patch('/api/v1/usuarios/me/', {'nome': 'Sem login'}, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cadastro_continua_exigindo_validacao_de_senha(self):
        dados = {
            'nome': 'Novo Cliente', 'cpf': '52998224725', 'email': 'novo@example.com', 'telefone': '51988887777',
            'data_nascimento': '2000-01-01', 'genero': 'M', 'password': '12345678', 'password_confirmacao': '12345678',
        }
        resposta = self.client.post('/api/v1/usuarios/cadastro/', dados, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Usuario.objects.filter(email='novo@example.com').exists())

    def test_token_hash_e_unico_no_banco(self):
        from django.db import IntegrityError, transaction
        token = self.criar_link()
        with self.assertRaises(IntegrityError), transaction.atomic():
            RedefinicaoSenha.objects.create(
                usuario=self.usuario, token_hash=redefinicao_senha.calcular_hash(token),
                data_expiracao=timezone.now() + timedelta(minutes=30),
            )

    def test_usuario_pode_ter_varias_redefinicoes_e_exclusao_remove_o_historico(self):
        self.criar_link()
        self.criar_link()
        self.assertEqual(self.usuario.redefinicoes_senha.count(), 2)

        self.usuario.delete()

        self.assertFalse(RedefinicaoSenha.objects.exists())

    def test_cascade_da_redefinicao_nao_apaga_pedidos(self):
        from django.db import models
        from agrostore.pedidos.models import PedidoCliente
        campo = PedidoCliente._meta.get_field('usuario')
        self.assertEqual(campo.remote_field.on_delete, models.PROTECT)
