from rest_framework import status
from rest_framework.test import APITestCase

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

    def test_produtor_atualiza_apenas_descricao_e_status_da_loja(self):
        self.client.post('/api/v1/lojas/lojas/', {'nome': 'Feira Central', 'cnpj': '98765432000199'}, format='json')

        response = self.client.patch('/api/v1/lojas/me/', {'descricao': 'Produtos da estação', 'ativa': False}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['descricao'], 'Produtos da estação')
        self.assertFalse(response.data['ativa'])

        response = self.client.patch('/api/v1/lojas/me/', {'nome': 'Outro nome'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
