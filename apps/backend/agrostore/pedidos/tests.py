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

        self.assertFalse(Carrinho.objects.filter(pk=item_b.carrinho_id).exists())
        carrinho_a = Carrinho.objects.get(pk=item_a.carrinho_id)
        self.assertEqual(carrinho_a.valor_bruto, Decimal('4.00'))
        self.assertEqual(carrinho_a.valor_liquido, Decimal('4.00'))

        pedido_a = Pedido.objects.get(loja=self.loja_a)
        self.assertEqual(pedido_a.cliente.nome, self.cliente.nome)
        self.assertEqual(pedido_a.itens.get().nome_produto, self.produto_a.nome)

    def test_checkout_de_todas_as_lojas_exclui_os_carrinhos_finalizados(self):
        item_a = self._adicionar_item(self.produto_a, 2)
        item_b = self._adicionar_item(self.produto_b, 3)

        response = self.client.post(
            '/api/v1/pedidos/',
            {'carrinho_produto_ids': [item_a.carrinho_produto_id, item_b.carrinho_produto_id]},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(Carrinho.objects.filter(usuario=self.cliente).exists())

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
        self.assertIsNotNone(response.data[0]['data_criacao'])

    def test_cliente_lista_pedidos_com_data_de_criacao(self):
        Pedido.objects.create(usuario=self.cliente, loja=self.loja_a, status=StatusPedido.objects.get(status='Pendente'))

        response = self.client.get('/api/v1/pedidos/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data_criacao', response.data[0])
        self.assertIsNotNone(response.data[0]['data_criacao'])

    def test_alteracao_do_perfil_preserva_snapshot_do_cliente_no_pedido(self):
        item = self._adicionar_item(self.produto_a, 1)
        checkout = self.client.post('/api/v1/pedidos/', {'carrinho_produto_ids': [item.carrinho_produto_id]}, format='json')
        nome_original = self.cliente.nome

        response = self.client.patch('/api/v1/usuarios/me/', {'nome': 'Nome Novo'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        pedido = Pedido.objects.get(pedido_id=checkout.data[0]['pedido_id'])
        self.assertEqual(pedido.cliente.nome, nome_original)

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

    def test_checkout_ajusta_ao_novo_estoque_o_carrinho_de_outro_cliente(self):
        item_outro_cliente = self._adicionar_item(self.produto_a, 9, usuario=self._criar_outro_cliente())
        item = self._adicionar_item(self.produto_a, 2)

        response = self.client.post('/api/v1/pedidos/', {'carrinho_produto_ids': [item.carrinho_produto_id]}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        item_outro_cliente.refresh_from_db()
        self.assertEqual(item_outro_cliente.quantidade, 8)
        self.assertEqual(item_outro_cliente.carrinho.valor_bruto, Decimal('40.00'))

    def test_rejeita_checkout_inteiro_com_item_sem_estoque_mesmo_apos_reposicao(self):
        item_sem_estoque = self._adicionar_item(self.produto_a, 0)
        item_valido = self._adicionar_item(self.produto_b, 1)

        response = self.client.post(
            '/api/v1/pedidos/',
            {'carrinho_produto_ids': [item_sem_estoque.carrinho_produto_id, item_valido.carrinho_produto_id]},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'O produto Alface está sem estoque. Remova-o da seleção para finalizar.')
        self.assertFalse(Pedido.objects.exists())
        self.produto_b.refresh_from_db()
        self.assertEqual(self.produto_b.estoque, 8)
        self.assertEqual(CarrinhoProduto.objects.count(), 2)

    def test_cancelamento_nao_restaura_quantidade_ajustada_no_carrinho(self):
        item_outro_cliente = self._adicionar_item(self.produto_a, 9, usuario=self._criar_outro_cliente())
        item = self._adicionar_item(self.produto_a, 2)
        checkout = self.client.post('/api/v1/pedidos/', {'carrinho_produto_ids': [item.carrinho_produto_id]}, format='json')

        response = self.client.patch(f'/api/v1/pedidos/{checkout.data[0]["pedido_id"]}/cancelar/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.produto_a.refresh_from_db()
        self.assertEqual(self.produto_a.estoque, 10)
        item_outro_cliente.refresh_from_db()
        self.assertEqual(item_outro_cliente.quantidade, 8)

    def _criar_outro_cliente(self):
        return Usuario.objects.create_user(
            cpf='22345678905',
            email='outro-estoque@example.com',
            password='senha123',
            nome='Outro Cliente Estoque',
            data_nascimento='1991-01-01',
            genero=self.genero,
        )

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

    def _adicionar_item(self, produto, quantidade, usuario=None):
        carrinho, _ = Carrinho.objects.get_or_create(usuario=usuario or self.cliente, loja=produto.loja)
        item = CarrinhoProduto.objects.create(carrinho=carrinho, produto=produto, quantidade=quantidade)
        carrinho.recalcular_totais()
        return item

    def _checkout(self, *itens):
        return self.client.post('/api/v1/pedidos/', {'carrinho_produto_ids': [item.carrinho_produto_id for item in itens]}, format='json')

    def test_checkout_ajusta_para_o_estoque_restante_e_preserva_carrinhos_iguais_ou_abaixo(self):
        item_acima = self._adicionar_item(self.produto_a, 9, usuario=self._criar_outro_cliente())
        item_igual = self._adicionar_item(self.produto_a, 2, usuario=self._criar_cliente_extra('1'))
        item_abaixo = self._adicionar_item(self.produto_a, 1, usuario=self._criar_cliente_extra('2'))
        atualizado_abaixo = item_abaixo.data_atualizacao
        item = self._adicionar_item(self.produto_a, 8)

        response = self._checkout(item)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.produto_a.refresh_from_db()
        self.assertEqual(self.produto_a.estoque, 2)
        for outro in (item_acima, item_igual, item_abaixo):
            outro.refresh_from_db()
        self.assertEqual([item_acima.quantidade, item_igual.quantidade, item_abaixo.quantidade], [2, 2, 1])
        self.assertEqual(item_abaixo.data_atualizacao, atualizado_abaixo)
        carrinho = Carrinho.objects.get(pk=item_acima.carrinho_id)
        self.assertEqual(
            (carrinho.valor_bruto, carrinho.valor_desconto, carrinho.valor_liquido),
            (Decimal('10.00'), Decimal('2.00'), Decimal('8.00')),
        )

    def test_checkout_que_zera_o_estoque_mantem_item_e_carrinho_de_outro_cliente_com_quantidade_zero(self):
        outro_cliente = self._criar_outro_cliente()
        item_outro_cliente = self._adicionar_item(self.produto_a, 6, usuario=outro_cliente)
        item_outro_produto = self._adicionar_item(self.produto_nao_selecionado, 2, usuario=outro_cliente)
        item = self._adicionar_item(self.produto_a, 10)

        response = self._checkout(item)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.produto_a.refresh_from_db()
        self.assertEqual(self.produto_a.estoque, 0)
        item_outro_cliente.refresh_from_db()
        item_outro_produto.refresh_from_db()
        self.assertEqual(item_outro_cliente.quantidade, 0)
        self.assertEqual(item_outro_produto.quantidade, 2)
        carrinho = Carrinho.objects.get(pk=item_outro_cliente.carrinho_id)
        self.assertEqual((carrinho.valor_bruto, carrinho.valor_liquido), (Decimal('8.00'), Decimal('8.00')))

        self.client.force_authenticate(outro_cliente)
        itens = self.client.get('/api/v1/carrinhos/').data[0]['itens']
        item_zerado = next(i for i in itens if i['produto'] == self.produto_a.produto_id)
        self.assertEqual((item_zerado['quantidade'], item_zerado['estoque'], item_zerado['disponivel']), (0, 0, False))

    def test_checkout_que_zera_o_estoque_deixa_carrinho_so_com_item_zerado_com_totais_zerados(self):
        item_outro_cliente = self._adicionar_item(self.produto_a, 4, usuario=self._criar_outro_cliente())
        item = self._adicionar_item(self.produto_a, 10)

        self._checkout(item)

        item_outro_cliente.refresh_from_db()
        self.assertEqual(item_outro_cliente.quantidade, 0)
        carrinho = Carrinho.objects.get(pk=item_outro_cliente.carrinho_id)
        self.assertEqual((carrinho.valor_bruto, carrinho.valor_desconto, carrinho.valor_liquido), (Decimal('0.00'),) * 3)

    def test_checkout_nao_altera_indevidamente_os_carrinhos_do_proprio_comprador(self):
        item = self._adicionar_item(self.produto_a, 2)
        item_mesma_loja = self._adicionar_item(self.produto_nao_selecionado, 6)
        item_outra_loja = self._adicionar_item(self.produto_b, 8)

        response = self._checkout(item)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(CarrinhoProduto.objects.filter(pk=item.pk).exists())
        item_mesma_loja.refresh_from_db()
        item_outra_loja.refresh_from_db()
        self.assertEqual(item_mesma_loja.quantidade, 6)
        self.assertEqual(item_outra_loja.quantidade, 8)
        self.assertEqual(Carrinho.objects.get(pk=item_mesma_loja.carrinho_id).valor_liquido, Decimal('24.00'))
        self.assertEqual(Carrinho.objects.get(pk=item_outra_loja.carrinho_id).valor_liquido, Decimal('56.00'))

    def test_checkout_com_varias_lojas_ajusta_os_carrinhos_de_outro_cliente_em_cada_loja(self):
        outro_cliente = self._criar_outro_cliente()
        outro_a = self._adicionar_item(self.produto_a, 10, usuario=outro_cliente)
        outro_b = self._adicionar_item(self.produto_b, 8, usuario=outro_cliente)
        item_a = self._adicionar_item(self.produto_a, 4)
        item_b = self._adicionar_item(self.produto_b, 8)

        response = self._checkout(item_a, item_b)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pedido.objects.count(), 2)
        outro_a.refresh_from_db()
        outro_b.refresh_from_db()
        self.assertEqual((outro_a.quantidade, outro_b.quantidade), (6, 0))
        self.assertEqual(Carrinho.objects.get(pk=outro_a.carrinho_id).valor_liquido, Decimal('24.00'))
        self.assertEqual(Carrinho.objects.get(pk=outro_b.carrinho_id).valor_liquido, Decimal('0.00'))

    def test_recusa_checkout_inteiro_com_item_de_produto_sem_estoque_e_nao_altera_nada(self):
        Produto.objects.filter(pk=self.produto_a.pk).update(estoque=0)
        item_zerado = self._adicionar_item(self.produto_a, 0)
        item_valido = self._adicionar_item(self.produto_b, 3)
        item_mesma_loja = self._adicionar_item(self.produto_nao_selecionado, 2)

        response = self._checkout(item_valido, item_zerado, item_mesma_loja)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'detail': 'O produto Alface está sem estoque. Remova-o da seleção para finalizar.'})
        self.assertFalse(Pedido.objects.exists())
        self.assertFalse(PedidoProduto.objects.exists())
        self.assertFalse(PedidoCliente.objects.exists())
        estoques = {p.pk: p.estoque for p in Produto.objects.all()}
        self.assertEqual(estoques[self.produto_a.pk], 0)
        self.assertEqual(estoques[self.produto_b.pk], 8)
        self.assertEqual(estoques[self.produto_nao_selecionado.pk], 6)
        quantidades = {i.pk: i.quantidade for i in CarrinhoProduto.objects.all()}
        self.assertEqual(quantidades, {item_zerado.pk: 0, item_valido.pk: 3, item_mesma_loja.pk: 2})

    def test_recusa_checkout_com_apenas_um_item_zerado(self):
        item_zerado = self._adicionar_item(self.produto_a, 0)

        response = self._checkout(item_zerado)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('sem estoque', response.data['detail'])
        self.assertFalse(Pedido.objects.exists())
        self.produto_a.refresh_from_db()
        self.assertEqual(self.produto_a.estoque, 10)

    def test_cliente_sobe_item_zerado_apos_reposicao_e_finaliza_o_pedido(self):
        item = self._adicionar_item(self.produto_a, 0)
        self.assertEqual(self._checkout(item).status_code, status.HTTP_400_BAD_REQUEST)

        atualizacao = self.client.patch(f'/api/v1/carrinhos/itens/{item.carrinho_produto_id}/', {'quantidade': 1}, format='json')
        response = self._checkout(item)

        self.assertEqual(atualizacao.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pedido.objects.count(), 1)
        self.produto_a.refresh_from_db()
        self.assertEqual(self.produto_a.estoque, 9)
        self.assertFalse(Carrinho.objects.filter(usuario=self.cliente).exists())

    def test_cancelamento_nao_restaura_item_zerado_de_outro_cliente_que_fica_disponivel(self):
        outro_cliente = self._criar_outro_cliente()
        item_outro_cliente = self._adicionar_item(self.produto_a, 4, usuario=outro_cliente)
        item = self._adicionar_item(self.produto_a, 10)
        checkout = self._checkout(item)

        cancelamento = self.client.patch(f'/api/v1/pedidos/{checkout.data[0]["pedido_id"]}/cancelar/')

        self.assertEqual(cancelamento.status_code, status.HTTP_200_OK)
        item_outro_cliente.refresh_from_db()
        self.assertEqual(item_outro_cliente.quantidade, 0)
        self.assertTrue(Carrinho.objects.filter(pk=item_outro_cliente.carrinho_id).exists())
        self.client.force_authenticate(outro_cliente)
        item_resposta = self.client.get('/api/v1/carrinhos/').data[0]['itens'][0]
        self.assertEqual((item_resposta['quantidade'], item_resposta['estoque'], item_resposta['disponivel']), (0, 10, True))

    def _criar_cliente_extra(self, sufixo):
        return Usuario.objects.create_user(
            cpf=f'2234567891{sufixo}',
            email=f'extra-estoque-{sufixo}@example.com',
            password='senha123',
            nome=f'Cliente Extra {sufixo}',
            data_nascimento='1991-01-01',
            genero=self.genero,
        )
