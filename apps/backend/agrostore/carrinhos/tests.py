from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase

from agrostore.carrinhos.models import Carrinho, CarrinhoProduto
from agrostore.lojas.models import Loja
from agrostore.produtos.models import Categoria, PrecoProduto, Produto
from agrostore.usuarios.models import Genero, Usuario


class CarrinhoAPITests(APITestCase):
    def setUp(self):
        self.genero, _ = Genero.objects.get_or_create(id_genero='M', defaults={'genero': 'Masculino'})
        self.cliente = Usuario.objects.create_user(
            cpf='12345678901',
            email='cliente@example.com',
            password='senha123',
            nome='Cliente Teste',
            data_nascimento='1990-01-01',
            genero=self.genero,
        )
        self.outro_cliente = Usuario.objects.create_user(
            cpf='12345678902',
            email='outro@example.com',
            password='senha123',
            nome='Outro Cliente',
            data_nascimento='1991-01-01',
            genero=self.genero,
        )
        self.produtor = Usuario.objects.create_user(
            cpf='12345678903',
            email='produtor@example.com',
            password='senha123',
            nome='Produtor Teste',
            data_nascimento='1980-01-01',
            genero=self.genero,
            is_produtor=True,
        )
        self.loja = Loja.objects.create(
            proprietario=self.produtor,
            nome='Loja Verde',
            cnpj='12345678000199',
        )
        self.categoria = Categoria.objects.create(nome='Frutas')
        self.produto = Produto.objects.create(
            loja=self.loja,
            nome='Maçã',
            estoque=10,
            sku='MACA-001',
            categoria=self.categoria,
        )
        PrecoProduto.objects.create(produto=self.produto, preco_venda=Decimal('10.00'), preco_desconto=Decimal('2.00'))
        self.client.force_authenticate(self.cliente)

    def test_adiciona_produto_ativo_com_estoque_suficiente(self):
        response = self.client.post('/api/v1/carrinhos/', {'produto': self.produto.produto_id, 'quantidade': 2}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CarrinhoProduto.objects.get().quantidade, 2)
        carrinho = Carrinho.objects.get()
        self.assertEqual(carrinho.valor_bruto, Decimal('20.00'))
        self.assertEqual(carrinho.valor_desconto, Decimal('4.00'))
        self.assertEqual(carrinho.valor_liquido, Decimal('16.00'))

    def test_rejeita_usuario_nao_autenticado(self):
        self.client.force_authenticate(user=None)

        response = self.client.post('/api/v1/carrinhos/', {'produto': self.produto.produto_id, 'quantidade': 1}, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(CarrinhoProduto.objects.exists())

    def test_rejeita_produto_inativo(self):
        self.produto.ativo = False
        self.produto.save(update_fields=['ativo'])

        response = self.client.post('/api/v1/carrinhos/', {'produto': self.produto.produto_id, 'quantidade': 1}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(CarrinhoProduto.objects.exists())

    def test_rejeita_quantidade_acima_do_estoque(self):
        response = self.client.post('/api/v1/carrinhos/', {'produto': self.produto.produto_id, 'quantidade': 11}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(CarrinhoProduto.objects.exists())

    def test_soma_quantidade_ao_adicionar_produto_repetido(self):
        self.client.post('/api/v1/carrinhos/', {'produto': self.produto.produto_id, 'quantidade': 2}, format='json')
        response = self.client.post('/api/v1/carrinhos/', {'produto': self.produto.produto_id, 'quantidade': 3}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CarrinhoProduto.objects.get().quantidade, 5)

    def test_lista_apenas_carrinhos_do_usuario_autenticado(self):
        self.client.post('/api/v1/carrinhos/', {'produto': self.produto.produto_id, 'quantidade': 1}, format='json')
        Carrinho.objects.create(usuario=self.outro_cliente, loja=self.loja)

        response = self.client.get('/api/v1/carrinhos/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['loja'], self.loja.loja_id)

    def test_nao_atualiza_item_de_outro_usuario(self):
        carrinho_outro_usuario = Carrinho.objects.create(usuario=self.outro_cliente, loja=self.loja)
        item_outro_usuario = CarrinhoProduto.objects.create(
            carrinho=carrinho_outro_usuario,
            produto=self.produto,
            quantidade=1,
        )

        response = self.client.patch(
            f'/api/v1/carrinhos/itens/{item_outro_usuario.carrinho_produto_id}/',
            {'quantidade': 2},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        item_outro_usuario.refresh_from_db()
        self.assertEqual(item_outro_usuario.quantidade, 1)

    def test_nao_remove_item_de_outro_usuario(self):
        carrinho_outro_usuario = Carrinho.objects.create(usuario=self.outro_cliente, loja=self.loja)
        item_outro_usuario = CarrinhoProduto.objects.create(
            carrinho=carrinho_outro_usuario,
            produto=self.produto,
            quantidade=1,
        )

        response = self.client.delete(f'/api/v1/carrinhos/itens/{item_outro_usuario.carrinho_produto_id}/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(CarrinhoProduto.objects.filter(carrinho_produto_id=item_outro_usuario.carrinho_produto_id).exists())
