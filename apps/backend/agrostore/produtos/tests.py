from django.db import IntegrityError
from django.db.models.deletion import ProtectedError
from rest_framework import status
from rest_framework.test import APITestCase

from agrostore.lojas.models import Loja
from agrostore.produtos.models import Categoria, Produto
from agrostore.usuarios.models import Genero, Usuario


class ProdutoCategoriaAPITests(APITestCase):
    def setUp(self):
        self.genero = Genero.objects.create(id_genero='M', genero='Masculino')
        self.produtor = self.criar_usuario('12345678901', 'produtor@example.com', is_produtor=True)
        self.cliente = self.criar_usuario('12345678902', 'cliente@example.com')
        self.administrador = self.criar_usuario('12345678903', 'admin@example.com', is_staff=True)
        self.loja = Loja.objects.create(
            proprietario=self.produtor,
            nome='Feira Verde',
            cnpj='12345678000199',
        )
        self.categoria_ativa = Categoria.objects.create(nome='Frutas')
        self.categoria_inativa = Categoria.objects.create(nome='Sugestão pendente', ativo=False)
        self.produto = Produto.objects.create(
            loja=self.loja,
            nome='Maçã',
            sku='MACA-001',
            estoque=10,
            categoria=self.categoria_ativa,
        )

    def criar_usuario(self, cpf, email, **extra_fields):
        return Usuario.objects.create_user(
            cpf=cpf,
            email=email,
            password='senha123',
            nome=email.split('@')[0],
            data_nascimento='1990-01-01',
            genero=self.genero,
            **extra_fields,
        )

    def produto_payload(self, **overrides):
        payload = {
            'loja': self.loja.loja_id,
            'nome': 'Banana',
            'sku': 'BANANA-001',
            'estoque': 5,
            'categoria': self.categoria_ativa.categoria_id,
        }
        payload.update(overrides)
        return payload

    def test_criacao_exige_categoria(self):
        self.client.force_authenticate(self.produtor)
        payload = self.produto_payload()
        payload.pop('categoria')

        response = self.client.post('/api/v1/produtos/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('categoria', response.data)

    def test_model_exige_categoria(self):
        with self.assertRaises(IntegrityError):
            Produto.objects.create(
                loja=self.loja,
                nome='Produto sem categoria',
                sku='SEM-CATEGORIA-001',
                estoque=1,
            )

    def test_criacao_rejeita_categoria_inativa(self):
        self.client.force_authenticate(self.produtor)

        response = self.client.post(
            '/api/v1/produtos/',
            self.produto_payload(categoria=self.categoria_inativa.categoria_id),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('categoria', response.data)

    def test_edicao_de_produto_com_categoria_inativa_e_permitida(self):
        self.produto.categoria = self.categoria_inativa
        self.produto.save(update_fields=['categoria'])
        self.client.force_authenticate(self.produtor)

        response = self.client.patch(
            f'/api/v1/produtos/{self.produto.produto_id}/',
            {'nome': 'Maçã orgânica'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.nome, 'Maçã orgânica')

    def test_troca_para_categoria_inativa_e_rejeitada(self):
        self.client.force_authenticate(self.produtor)

        response = self.client.patch(
            f'/api/v1/produtos/{self.produto.produto_id}/',
            {'categoria': self.categoria_inativa.categoria_id},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('categoria', response.data)

    def test_lista_filtra_por_categoria(self):
        outra_categoria = Categoria.objects.create(nome='Verduras')
        Produto.objects.create(
            loja=self.loja,
            nome='Alface',
            sku='ALFACE-001',
            estoque=4,
            categoria=outra_categoria,
        )

        response = self.client.get(f'/api/v1/produtos/?categoria={self.categoria_ativa.categoria_id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([produto['produto_id'] for produto in response.data], [self.produto.produto_id])

    def test_produtor_cria_sugestao_inativa(self):
        self.client.force_authenticate(self.produtor)

        response = self.client.post('/api/v1/produtos/categorias/', {'nome': 'Ervas', 'ativo': True}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data['ativo'])

    def test_administrador_pode_criar_categoria_ativa(self):
        self.client.force_authenticate(self.administrador)

        response = self.client.post('/api/v1/produtos/categorias/', {'nome': 'Laticínios', 'ativo': True}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['ativo'])

    def test_cliente_nao_cria_sugestao(self):
        self.client.force_authenticate(self.cliente)

        response = self.client.post('/api/v1/produtos/categorias/', {'nome': 'Ervas'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sugestoes_inativas_sao_publicas_e_filtro_retorna_apenas_ativas(self):
        response = self.client.get('/api/v1/produtos/categorias/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        response = self.client.get('/api/v1/produtos/categorias/?ativo=true')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([categoria['nome'] for categoria in response.data], ['Frutas'])

    def test_somente_administrador_altera_categoria(self):
        self.client.force_authenticate(self.produtor)

        response = self.client.patch(
            f'/api/v1/produtos/categorias/{self.categoria_inativa.categoria_id}/',
            {'ativo': True},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.administrador)
        response = self.client.patch(
            f'/api/v1/produtos/categorias/{self.categoria_inativa.categoria_id}/',
            {'ativo': True},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['ativo'])

    def test_categoria_nao_pode_ser_excluida(self):
        self.client.force_authenticate(self.administrador)

        response = self.client.delete(f'/api/v1/produtos/categorias/{self.categoria_ativa.categoria_id}/')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(Categoria.objects.filter(categoria_id=self.categoria_ativa.categoria_id).exists())

    def test_model_protege_categoria_com_produtos_vinculados(self):
        with self.assertRaises(ProtectedError):
            self.categoria_ativa.delete()
