from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase

from agrostore.carrinhos.models import Carrinho, CarrinhoProduto
from agrostore.lojas.models import Loja
from agrostore.pedidos.models import Pedido, PedidoProduto, StatusPedido
from agrostore.produtos.models import Categoria, PrecoProduto, Produto
from agrostore.usuarios.models import Genero, Usuario


class PedidoCheckoutTests(APITestCase):
    def setUp(self):
        self.genero = Genero.objects.create(id_genero='F', genero='Feminino')
        self.cliente = Usuario.objects.create_user(
            cpf='22345678901',
            email='cliente-pedido@example.com',
            password='senha123',
            nome='Cliente Pedido',
            data_nascimento='1990-01-01',
            genero=self.genero,
        )
        self.produtor = Usuario.objects.create_user(
            cpf='22345678902',
            email='produtor-pedido@example.com',
            password='senha123',
            nome='Produtor Pedido',
            data_nascimento='1980-01-01',
            genero=self.genero,
            is_produtor=True,
        )
        self.categoria = Categoria.objects.create(nome='Verduras')
        self.loja_a = Loja.objects.create(proprietario=self.produtor, nome='Loja A', cnpj='22345678000199')
        self.loja_b = Loja.objects.create(proprietario=self.produtor, nome='Loja B', cnpj='22345678000198')
        self.produto_a = self._criar_produto(self.loja_a, 'Alface', 'ALF-001', 10, Decimal('5.00'), Decimal('1.00'))
        self.produto_b = self._criar_produto(self.loja_b, 'Cenoura', 'CEN-001', 8, Decimal('7.00'), Decimal('0.00'))
        self.produto_nao_selecionado = self._criar_produto(self.loja_a, 'Rúcula', 'RUC-001', 6, Decimal('4.00'), Decimal('0.00'))
        StatusPedido.objects.get_or_create(status='Pendente')
        self.client.force_authenticate(self.cliente)

    def test_finaliza_itens_selecionados_criando_pedidos_por_loja_e_baixando_estoque(self):
        item_a = self._adicionar_item(self.produto_a, 2)
        item_b = self._adicionar_item(self.produto_b, 3)
        item_nao_selecionado = self._adicionar_item(self.produto_nao_selecionado, 1)

        response = self.client.post(
            '/api/v1/pedidos/',
            {'carrinho_produto_ids': [item_a.carrinho_produto_id, item_b.carrinho_produto_id]},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pedido.objects.count(), 2)
        self.assertEqual(PedidoProduto.objects.count(), 2)

        self.produto_a.refresh_from_db()
        self.produto_b.refresh_from_db()
        self.assertEqual(self.produto_a.estoque, 8)
        self.assertEqual(self.produto_b.estoque, 5)

        self.assertFalse(CarrinhoProduto.objects.filter(carrinho_produto_id=item_a.carrinho_produto_id).exists())
        self.assertFalse(CarrinhoProduto.objects.filter(carrinho_produto_id=item_b.carrinho_produto_id).exists())
        self.assertTrue(CarrinhoProduto.objects.filter(carrinho_produto_id=item_nao_selecionado.carrinho_produto_id).exists())

    def test_rejeita_checkout_com_estoque_insuficiente(self):
        item = self._adicionar_item(self.produto_a, 2)
        self.produto_a.estoque = 1
        self.produto_a.save(update_fields=['estoque'])

        response = self.client.post(
            '/api/v1/pedidos/',
            {'carrinho_produto_ids': [item.carrinho_produto_id]},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Pedido.objects.exists())

    def _criar_produto(self, loja, nome, sku, estoque, preco_venda, preco_desconto):
        produto = Produto.objects.create(
            loja=loja,
            nome=nome,
            estoque=estoque,
            sku=sku,
            categoria=self.categoria,
        )
        PrecoProduto.objects.create(produto=produto, preco_venda=preco_venda, preco_desconto=preco_desconto)
        return produto

    def _adicionar_item(self, produto, quantidade):
        carrinho, _ = Carrinho.objects.get_or_create(usuario=self.cliente, loja=produto.loja)
        item = CarrinhoProduto.objects.create(carrinho=carrinho, produto=produto, quantidade=quantidade)
        carrinho.recalcular_totais()
        return item
