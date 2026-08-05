from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase

from agrostore.lojas.models import Loja
from agrostore.produtos.models import Categoria, PrecoProduto, Produto
from agrostore.usuarios.models import Genero, Usuario


class FavoritoAPITests(APITestCase):
    def setUp(self):
        self.genero, _ = Genero.objects.get_or_create(id_genero='M', defaults={'genero': 'Masculino'})
        self.produtor = self.criar_usuario('12345678901', 'produtor@example.com', is_produtor=True)
        self.cliente = self.criar_usuario('12345678902', 'cliente@example.com')
        self.outro_cliente = self.criar_usuario('12345678903', 'outro-cliente@example.com')
        self.loja = Loja.objects.create(proprietario=self.produtor, nome='Feira Verde', cnpj='12345678000199')
        self.categoria = Categoria.objects.create(nome='Frutas')
        self.produto = Produto.objects.create(
            loja=self.loja,
            nome='Maçã',
            descricao='Produção local',
            sku='MACA-001',
            estoque=8,
            categoria=self.categoria,
        )
        PrecoProduto.objects.create(produto=self.produto, preco_venda=Decimal('10.00'), porcentagem_desconto=10)

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

    def test_endpoints_exigem_autenticacao(self):
        response = self.client.get('/api/v1/favoritos/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post('/api/v1/favoritos/', {'produto': self.produto.produto_id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cliente_cria_favorito_e_recebe_dados_completos_do_produto(self):
        self.client.force_authenticate(self.cliente)

        response = self.client.post('/api/v1/favoritos/', {'produto': self.produto.produto_id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['produto'], self.produto.produto_id)
        self.assertIn('data_criacao', response.data)
        dados_produto = response.data['dados_produto']
        self.assertEqual(dados_produto['produto_id'], self.produto.produto_id)
        self.assertEqual(dados_produto['nome'], 'Maçã')
        self.assertEqual(dados_produto['loja_nome'], 'Feira Verde')
        self.assertEqual(dados_produto['categoria_nome'], 'Frutas')
        self.assertEqual(dados_produto['estoque'], 8)
        self.assertTrue(dados_produto['ativo'])
        self.assertTrue(dados_produto['disponivel'])
        self.assertEqual(dados_produto['preco'], Decimal('9.00'))

    def test_listagem_retorna_apenas_favoritos_do_usuario_autenticado(self):
        self.client.force_authenticate(self.cliente)
        criado = self.client.post('/api/v1/favoritos/', {'produto': self.produto.produto_id}, format='json')
        self.assertEqual(criado.status_code, status.HTTP_201_CREATED)

        self.client.force_authenticate(self.outro_cliente)
        response = self.client.get('/api/v1/favoritos/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_produto_nao_pode_ser_favoritado_duas_vezes(self):
        self.client.force_authenticate(self.cliente)
        self.client.post('/api/v1/favoritos/', {'produto': self.produto.produto_id}, format='json')

        response = self.client.post('/api/v1/favoritos/', {'produto': self.produto.produto_id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_usuario_remove_apenas_o_proprio_favorito(self):
        self.client.force_authenticate(self.cliente)
        criado = self.client.post('/api/v1/favoritos/', {'produto': self.produto.produto_id}, format='json')
        favorito_id = criado.data['favorito_id']

        self.client.force_authenticate(self.outro_cliente)
        response = self.client.delete(f'/api/v1/favoritos/{favorito_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.client.force_authenticate(self.cliente)
        response = self.client.delete(f'/api/v1/favoritos/{favorito_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
