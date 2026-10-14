from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase

from agrostore.carrinhos.models import Carrinho, CarrinhoProduto
from agrostore.lojas.models import Loja
from agrostore.pedidos.models import Pedido, PedidoCliente, PedidoProduto, StatusPedido
from agrostore.produtos.models import Categoria, PrecoProduto, Produto
from agrostore.usuarios.models import Genero, Usuario


class PedidoCheckoutTests(APITestCase):
    def setUp(self):
        self.genero, _ = Genero.objects.get_or_create(id_genero='F', defaults={'genero': 'Feminino'})
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

        pedido_a = Pedido.objects.get(loja=self.loja_a)
        self.assertEqual(pedido_a.cliente.nome, self.cliente.nome)
        self.assertEqual(pedido_a.itens.get().nome_produto, self.produto_a.nome)

    def test_rejeita_checkout_sem_autenticacao(self):
        item = self._adicionar_item(self.produto_a, 1)
        self.client.force_authenticate(user=None)

        response = self.client.post(
            '/api/v1/pedidos/',
            {'carrinho_produto_ids': [item.carrinho_produto_id]},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Pedido.objects.exists())
        self.assertTrue(CarrinhoProduto.objects.filter(carrinho_produto_id=item.carrinho_produto_id).exists())

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

    def test_rejeita_checkout_com_produto_inativo(self):
        item = self._adicionar_item(self.produto_a, 1)
        self.produto_a.ativo = False
        self.produto_a.save(update_fields=['ativo'])

        response = self.client.post(
            '/api/v1/pedidos/',
            {'carrinho_produto_ids': [item.carrinho_produto_id]},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Pedido.objects.exists())
        self.assertTrue(CarrinhoProduto.objects.filter(carrinho_produto_id=item.carrinho_produto_id).exists())

    def test_rejeita_checkout_com_loja_inativa(self):
        item = self._adicionar_item(self.produto_a, 1)
        self.loja_a.ativa = False
        self.loja_a.save(update_fields=['ativa'])

        response = self.client.post(
            '/api/v1/pedidos/',
            {'carrinho_produto_ids': [item.carrinho_produto_id]},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Pedido.objects.exists())
        self.assertTrue(CarrinhoProduto.objects.filter(carrinho_produto_id=item.carrinho_produto_id).exists())

    def test_rejeita_checkout_sem_itens_selecionados(self):
        response = self.client.post('/api/v1/pedidos/', {'carrinho_produto_ids': []}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Pedido.objects.exists())

    def test_rejeita_checkout_com_item_invalido(self):
        response = self.client.post('/api/v1/pedidos/', {'carrinho_produto_ids': [999999]}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Pedido.objects.exists())

    def test_rejeita_checkout_com_item_de_outro_usuario(self):
        outro_cliente = Usuario.objects.create_user(
            cpf='22345678903',
            email='outro-pedido@example.com',
            password='senha123',
            nome='Outro Cliente',
            data_nascimento='1991-01-01',
            genero=self.genero,
        )
        carrinho_outro_usuario = Carrinho.objects.create(usuario=outro_cliente, loja=self.loja_a)
        item_outro_usuario = CarrinhoProduto.objects.create(
            carrinho=carrinho_outro_usuario,
            produto=self.produto_a,
            quantidade=1,
        )

        response = self.client.post(
            '/api/v1/pedidos/',
            {'carrinho_produto_ids': [item_outro_usuario.carrinho_produto_id]},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Pedido.objects.exists())
        self.assertTrue(CarrinhoProduto.objects.filter(carrinho_produto_id=item_outro_usuario.carrinho_produto_id).exists())

    def test_produtor_visualiza_apenas_pedidos_da_propria_loja_com_contato_minimo(self):
        pedido = Pedido.objects.create(
            usuario=self.cliente,
            loja=self.loja_a,
            status=StatusPedido.objects.get(status='Pendente'),
        )
        PedidoProduto.objects.create(
            pedido=pedido,
            produto=self.produto_a,
            nome_produto=self.produto_a.nome,
            quantidade=1,
            valor_unitario='5.00',
            subtotal='4.00',
        )
        PedidoCliente.objects.create(
            pedido=pedido,
            nome=self.cliente.nome,
            cpf=self.cliente.cpf,
            email=self.cliente.email,
            telefone=self.cliente.telefone,
            data_nascimento=self.cliente.data_nascimento,
            genero=str(self.cliente.genero),
        )
        self.client.force_authenticate(self.produtor)

        response = self.client.get('/api/v1/pedidos/minha-loja/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['cliente'], {'nome': self.cliente.nome, 'telefone': self.cliente.telefone})

    def test_produtor_respeita_fluxo_de_status(self):
        em_preparo = StatusPedido.objects.create(status='Em preparo')
        pronto = StatusPedido.objects.create(status='Pronto para retirada')
        pedido = Pedido.objects.create(
            usuario=self.cliente,
            loja=self.loja_a,
            status=StatusPedido.objects.get(status='Pendente'),
        )
        self.client.force_authenticate(self.produtor)

        response = self.client.patch(f'/api/v1/pedidos/{pedido.pedido_id}/status/', {'status': pronto.status_pedido_id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.patch(
            f'/api/v1/pedidos/{pedido.pedido_id}/status/',
            {'status': em_preparo.status_pedido_id},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cliente_cancela_pedido_pendente_e_restaura_estoque(self):
        item = self._adicionar_item(self.produto_a, 2)
        checkout = self.client.post(
            '/api/v1/pedidos/',
            {'carrinho_produto_ids': [item.carrinho_produto_id]},
            format='json',
        )
        pedido_id = checkout.data[0]['pedido_id']

        response = self.client.patch(f'/api/v1/pedidos/{pedido_id}/cancelar/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status_nome'], 'Cancelado')
        self.produto_a.refresh_from_db()
        self.assertEqual(self.produto_a.estoque, 10)

        response = self.client.patch(f'/api/v1/pedidos/{pedido_id}/cancelar/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.produto_a.refresh_from_db()
        self.assertEqual(self.produto_a.estoque, 10)

    def test_cliente_nao_cancela_pedido_de_outro_usuario(self):
        pedido = Pedido.objects.create(
            usuario=self.cliente,
            loja=self.loja_a,
            status=StatusPedido.objects.get(status='Pendente'),
        )
        outro_cliente = Usuario.objects.create_user(
            cpf='22345678904',
            email='outro-cancelamento@example.com',
            password='senha123',
            nome='Outro Cliente',
            data_nascimento='1991-01-01',
            genero=self.genero,
        )
        self.client.force_authenticate(outro_cliente)

        response = self.client.patch(f'/api/v1/pedidos/{pedido.pedido_id}/cancelar/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cliente_nao_cancela_pedido_em_preparo(self):
        pedido = Pedido.objects.create(
            usuario=self.cliente,
            loja=self.loja_a,
            status=StatusPedido.objects.create(status='Em preparo'),
        )

        response = self.client.patch(f'/api/v1/pedidos/{pedido.pedido_id}/cancelar/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancelamento_do_produtor_restaura_estoque(self):
        item = self._adicionar_item(self.produto_a, 2)
        checkout = self.client.post(
            '/api/v1/pedidos/',
            {'carrinho_produto_ids': [item.carrinho_produto_id]},
            format='json',
        )
        pedido_id = checkout.data[0]['pedido_id']
        status_cancelado = StatusPedido.objects.get(status='Cancelado')
        self.client.force_authenticate(self.produtor)

        response = self.client.patch(
            f'/api/v1/pedidos/{pedido_id}/status/',
            {'status': status_cancelado.status_pedido_id},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.produto_a.refresh_from_db()
        self.assertEqual(self.produto_a.estoque, 10)

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
