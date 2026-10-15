import os
import shutil
import tempfile
from unittest import mock

from django.core.exceptions import ValidationError
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

    def test_produtor_nao_altera_loja_de_outro_produtor_pelo_id(self):
        loja = Loja.objects.create(
            proprietario=self.produtor, nome='Feira Central', cnpj='98765432000199', descricao='Produtos coloniais', ativa=True,
        )
        outro_produtor = Usuario.objects.create_user(
            cpf='98765432133',
            email='loja-outro-produtor@example.com',
            password='senha123',
            nome='Outro Produtor',
            data_nascimento='1980-01-01',
            genero=self.produtor.genero,
            is_produtor=True,
        )
        self.client.force_authenticate(outro_produtor)

        response = self.client.patch(
            f'/api/v1/lojas/lojas/{loja.loja_id}/', {'nome': 'Invadida', 'descricao': 'x', 'ativa': False}, format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        loja.refresh_from_db()
        self.assertEqual(loja.nome, 'Feira Central')
        self.assertEqual(loja.descricao, 'Produtos coloniais')
        self.assertTrue(loja.ativa)

    def test_dono_tambem_recebe_405_no_patch_por_id(self):
        loja = Loja.objects.create(
            proprietario=self.produtor, nome='Feira Central', cnpj='98765432000199', descricao='Produtos coloniais', ativa=True,
        )

        response = self.client.patch(
            f'/api/v1/lojas/lojas/{loja.loja_id}/', {'nome': 'Novo nome', 'descricao': 'y', 'ativa': False}, format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        loja.refresh_from_db()
        self.assertEqual(loja.nome, 'Feira Central')
        self.assertEqual(loja.descricao, 'Produtos coloniais')
        self.assertTrue(loja.ativa)


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


@override_settings(MEDIA_ROOT=MEDIA_ROOT_TESTES_LOJA)
class LojaImagemPerfilSomenteLeituraAPITests(APITestCase):
    """Trava provisória: até a BE-018, imagem_perfil não é gravada pela API (somente leitura no LojaSerializer e recusada em /lojas/me/)."""

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT_TESTES_LOJA, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        genero, _ = Genero.objects.get_or_create(id_genero='M', defaults={'genero': 'Masculino'})
        self.produtor = Usuario.objects.create_user(
            cpf='98765432122', email='loja-trava@example.com', password='senha123',
            nome='Produtor Trava', data_nascimento='1980-01-01', genero=genero, is_produtor=True,
        )
        self.client.force_authenticate(self.produtor)

    def arquivo_png(self):
        return SimpleUploadedFile('fachada.png', PNG_VALIDO_LOJA, content_type='image/png')

    def arquivos_gravados(self):
        return [nome for _, _, nomes in os.walk(MEDIA_ROOT_TESTES_LOJA) for nome in nomes]

    def test_patch_me_recusa_imagem_perfil_e_nao_grava_arquivo(self):
        loja = Loja.objects.create(
            proprietario=self.produtor, nome='Feira Trava', cnpj='98765432000122', descricao='Descrição original',
            imagem_perfil='lojas/perfil/legado.jpg',
        )

        response = self.client.patch(
            '/api/v1/lojas/me/',
            {'descricao': 'Nova descrição', 'imagem_perfil': self.arquivo_png()},
            format='multipart',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Somente nome, descrição e status da loja podem ser alterados nesta área.')
        loja.refresh_from_db()
        self.assertEqual(loja.descricao, 'Descrição original')
        self.assertEqual(loja.imagem_perfil.name, 'lojas/perfil/legado.jpg')
        self.assertEqual(self.arquivos_gravados(), [])

    def test_post_multipart_cria_loja_sem_gravar_imagem(self):
        response = self.client.post(
            '/api/v1/lojas/lojas/',
            {'nome': 'Feira Nova', 'cnpj': '98765432000133', 'ativa': 'true', 'imagem_perfil': self.arquivo_png()},
            format='multipart',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        loja = Loja.objects.get(cnpj='98765432000133')
        self.assertEqual(loja.imagem_perfil.name, '')
        self.assertIsNone(response.data['imagem_perfil'])
        self.assertEqual(self.arquivos_gravados(), [])


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
