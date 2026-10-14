from datetime import date, timedelta

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Genero, Usuario


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
