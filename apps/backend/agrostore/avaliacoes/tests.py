from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from agrostore.avaliacoes.models import Avaliacao
from agrostore.avaliacoes.serializers import abreviar_nome
from agrostore.lojas.models import Loja
from agrostore.pedidos.models import Pedido, PedidoCliente, PedidoProduto, StatusPedido
from agrostore.produtos.models import Categoria, Produto
from agrostore.usuarios.models import Genero, Usuario


class AvaliacaoPedidoTests(APITestCase):
    def setUp(self):
        self.genero, _ = Genero.objects.get_or_create(id_genero='F', defaults={'genero': 'Feminino'})
        self.cliente = self._criar_usuario('32345678901', 'cliente-avaliacao@example.com')
        self.outro_cliente = self._criar_usuario('32345678902', 'outro-avaliacao@example.com')
        produtor = self._criar_usuario('32345678903', 'produtor-avaliacao@example.com', is_produtor=True)
        loja = Loja.objects.create(proprietario=produtor, nome='Loja Avaliada', cnpj='32345678000199')
        categoria = Categoria.objects.create(nome='Frutas')
        self.produto = Produto.objects.create(loja=loja, nome='Maçã', estoque=10, sku='MAC-001', categoria=categoria)
        entregue = StatusPedido.objects.create(status='Entregue')
        self.pedido = Pedido.objects.create(loja=loja, status=entregue)
        PedidoCliente.objects.create(
            pedido=self.pedido,
            usuario=self.cliente,
            nome=self.cliente.nome,
            cpf=self.cliente.cpf,
            email=self.cliente.email,
            data_nascimento=self.cliente.data_nascimento,
            genero=str(self.genero),
        )
        self.item = PedidoProduto.objects.create(
            pedido=self.pedido,
            produto=self.produto,
            nome_produto=self.produto.nome,
            quantidade=1,
            valor_unitario=Decimal('5.00'),
            subtotal=Decimal('5.00'),
        )

    def test_titular_do_pedido_avalia_item_entregue(self):
        self.client.force_authenticate(self.cliente)

        response = self.client.post('/api/v1/avaliacoes/', {'pedido_produto': self.item.pedido_produto_id, 'nota': 5}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        avaliacao = Avaliacao.objects.get()
        self.assertEqual(avaliacao.usuario, self.cliente)
        self.assertEqual(avaliacao.produto, self.produto)

    def test_avaliacao_de_item_de_pedido_de_outro_cliente_e_bloqueada(self):
        self.client.force_authenticate(self.outro_cliente)

        response = self.client.post('/api/v1/avaliacoes/', {'pedido_produto': self.item.pedido_produto_id, 'nota': 5}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('pedido_produto', response.data)
        self.assertFalse(Avaliacao.objects.exists())

    def test_nome_do_avaliador_e_abreviado(self):
        self.assertEqual(abreviar_nome('Maria da Silva Souza'), 'Maria S.')
        self.assertEqual(abreviar_nome('Maria'), 'Maria')
        self.assertEqual(abreviar_nome(''), '')

    def test_listagem_publica_exibe_nome_abreviado_do_avaliador(self):
        self.cliente.nome = 'Maria da Silva Souza'
        self.cliente.save()
        self._avaliar()

        response = self.client.get(f'/api/v1/avaliacoes/?produto={self.produto.produto_id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['usuario_nome'], 'Maria S.')

    def test_comentario_acima_de_500_caracteres_e_recusado(self):
        self.client.force_authenticate(self.cliente)

        response = self.client.post(
            '/api/v1/avaliacoes/',
            {'pedido_produto': self.item.pedido_produto_id, 'nota': 4, 'comentario': 'a' * 501},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['comentario'], ['O comentário deve ter no máximo 500 caracteres.'])
        self.assertFalse(Avaliacao.objects.exists())

    def test_comentario_com_500_caracteres_e_aceito(self):
        self.client.force_authenticate(self.cliente)

        response = self.client.post(
            '/api/v1/avaliacoes/',
            {'pedido_produto': self.item.pedido_produto_id, 'nota': 4, 'comentario': 'a' * 500},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_item_ja_avaliado_e_recusado_com_mensagem_da_regra(self):
        self._avaliar()
        self.client.force_authenticate(self.cliente)

        response = self.client.post('/api/v1/avaliacoes/', {'pedido_produto': self.item.pedido_produto_id, 'nota': 3}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['pedido_produto'], ['Este item já foi avaliado.'])
        self.assertEqual(Avaliacao.objects.count(), 1)

    def test_item_avaliado_de_outro_cliente_nao_revela_a_avaliacao(self):
        self._avaliar()
        self.client.force_authenticate(self.outro_cliente)

        response = self.client.post('/api/v1/avaliacoes/', {'pedido_produto': self.item.pedido_produto_id, 'nota': 3}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['pedido_produto'], ['Este item não pertence ao seu pedido.'])

    def test_admin_nao_inclui_nem_edita_avaliacao(self):
        avaliacao = self._avaliar()
        self.client.force_login(self._criar_administrador())

        inclusao = self.client.get(reverse('admin:avaliacoes_avaliacao_add'))
        edicao = self.client.post(reverse('admin:avaliacoes_avaliacao_change', args=[avaliacao.pk]), {'nota': 1, 'comentario': 'Alterado'})

        self.assertEqual(inclusao.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(edicao.status_code, status.HTTP_403_FORBIDDEN)
        avaliacao.refresh_from_db()
        self.assertEqual((avaliacao.nota, avaliacao.comentario), (5, 'Muito bom'))

    def test_admin_exclui_avaliacao_e_item_pode_ser_avaliado_de_novo(self):
        avaliacao = self._avaliar()
        self.client.force_login(self._criar_administrador())

        exclusao = self.client.post(reverse('admin:avaliacoes_avaliacao_delete', args=[avaliacao.pk]), {'post': 'yes'})

        self.assertEqual(exclusao.status_code, status.HTTP_302_FOUND)
        self.assertFalse(Avaliacao.objects.exists())
        self.client.force_authenticate(self.cliente)
        response = self.client.post('/api/v1/avaliacoes/', {'pedido_produto': self.item.pedido_produto_id, 'nota': 4}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_pedido_em_status_diferente_de_entregue_e_recusado(self):
        self.client.force_authenticate(self.cliente)
        for nome_status in ['Pendente', 'Em preparo', 'Pronto para retirada', 'Cancelado']:
            with self.subTest(status=nome_status):
                item = self._criar_item(self.cliente, nome_status)

                response = self._postar(item, 5)

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(response.data['pedido_produto'], ['Só é possível avaliar pedidos entregues.'])
        self.assertFalse(Avaliacao.objects.exists())

    def test_nota_fora_do_intervalo_ou_decimal_e_recusada(self):
        self.client.force_authenticate(self.cliente)
        for nota in [0, 6, 4.5, -1]:
            with self.subTest(nota=nota):
                response = self._postar(self.item, nota)

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn('nota', response.data)
        self.assertFalse(Avaliacao.objects.exists())

    def test_nota_e_obrigatoria(self):
        self.client.force_authenticate(self.cliente)

        response = self.client.post('/api/v1/avaliacoes/', {'pedido_produto': self.item.pedido_produto_id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nota', response.data)

    def test_comentario_em_branco_ou_ausente_e_aceito(self):
        self.client.force_authenticate(self.cliente)
        item_sem_comentario = self._criar_item(self.cliente, 'Entregue')

        em_branco = self.client.post(
            '/api/v1/avaliacoes/', {'pedido_produto': self.item.pedido_produto_id, 'nota': 3, 'comentario': ''}, format='json'
        )
        ausente = self._postar(item_sem_comentario, 3)

        self.assertEqual(em_branco.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ausente.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Avaliacao.objects.get(pedido_produto=self.item).comentario, '')

    def test_envio_sem_autenticacao_e_recusado(self):
        response = self._postar(self.item, 5)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Avaliacao.objects.exists())

    def test_listagem_publica_sem_autenticacao_filtra_por_produto(self):
        self._avaliar()
        outro_item = self._criar_item(self.cliente, 'Entregue', produto=self._criar_produto('Pera', 'PER-001'))
        Avaliacao.objects.create(usuario=self.cliente, produto=outro_item.produto, pedido_produto=outro_item, nota=2)

        todas = self.client.get('/api/v1/avaliacoes/')
        filtrada = self.client.get(f'/api/v1/avaliacoes/?produto={self.produto.produto_id}')

        self.assertEqual(todas.status_code, status.HTTP_200_OK)
        self.assertEqual(len(todas.data), 2)
        self.assertEqual(filtrada.status_code, status.HTTP_200_OK)
        self.assertEqual([a['produto'] for a in filtrada.data], [self.produto.produto_id])

    def test_produtor_que_comprou_e_recebeu_o_pedido_avalia_o_item(self):
        outro_produtor = self._criar_usuario('32345678908', 'outro-produtor-avaliacao@example.com', is_produtor=True)
        loja_alheia = Loja.objects.create(proprietario=outro_produtor, nome='Loja Alheia', cnpj='32345678000188')
        produto_alheio = self._criar_produto('Uva', 'UVA-001', loja=loja_alheia)
        produtor = self.produto.loja.proprietario
        item = self._criar_item(produtor, 'Entregue', produto=produto_alheio)
        self.client.force_authenticate(produtor)

        response = self._postar(item, 4)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Avaliacao.objects.get().usuario, produtor)

    def test_mesmo_produto_em_dois_pedidos_entregues_tem_uma_avaliacao_por_item(self):
        segundo_item = self._criar_item(self.cliente, 'Entregue')
        self.client.force_authenticate(self.cliente)

        primeira = self._postar(self.item, 5)
        segunda = self._postar(segundo_item, 3)
        repetida = self._postar(segundo_item, 1)

        self.assertEqual(primeira.status_code, status.HTTP_201_CREATED)
        self.assertEqual(segunda.status_code, status.HTTP_201_CREATED)
        self.assertEqual(repetida.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Avaliacao.objects.filter(produto=self.produto).count(), 2)

    def test_produto_e_autor_sao_definidos_pelo_backend(self):
        outro_produto = self._criar_produto('Pera', 'PER-002')
        self.client.force_authenticate(self.cliente)

        response = self.client.post(
            '/api/v1/avaliacoes/',
            {
                'pedido_produto': self.item.pedido_produto_id,
                'nota': 5,
                'produto': outro_produto.produto_id,
                'usuario': self.outro_cliente.pk,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        avaliacao = Avaliacao.objects.get()
        self.assertEqual(avaliacao.produto, self.produto)
        self.assertEqual(avaliacao.usuario, self.cliente)

    def test_put_patch_e_delete_pela_api_sao_recusados(self):
        avaliacao = self._avaliar()
        self.client.force_authenticate(self.cliente)
        url = f'/api/v1/avaliacoes/{avaliacao.avaliacao_id}/'

        for metodo in [self.client.put, self.client.patch]:
            self.assertEqual(metodo(url, {'nota': 1}, format='json').status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.delete(url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        avaliacao.refresh_from_db()
        self.assertEqual(avaliacao.nota, 5)

    def test_avaliacoes_de_produto_e_loja_inativos_continuam_na_listagem_publica(self):
        self._avaliar()
        Produto.objects.filter(pk=self.produto.pk).update(ativo=False)
        Loja.objects.filter(pk=self.produto.loja_id).update(ativa=False)

        response = self.client.get(f'/api/v1/avaliacoes/?produto={self.produto.produto_id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_item_de_outro_cliente_devolve_sempre_a_mesma_mensagem(self):
        item_avaliado = self._criar_item(self.cliente, 'Entregue')
        Avaliacao.objects.create(usuario=self.cliente, produto=self.produto, pedido_produto=item_avaliado, nota=5)
        item_pendente = self._criar_item(self.cliente, 'Pendente')
        self.client.force_authenticate(self.outro_cliente)

        for item in [self.item, item_avaliado, item_pendente]:
            with self.subTest(item=item.pedido_produto_id):
                response = self._postar(item, 3)

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(response.data['pedido_produto'], ['Este item não pertence ao seu pedido.'])

        with self.subTest(item='inexistente'):
            id_inexistente = PedidoProduto.objects.order_by('-pk').first().pk + 1000
            response = self.client.post('/api/v1/avaliacoes/', {'pedido_produto': id_inexistente, 'nota': 3}, format='json')

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data['pedido_produto'], ['Este item não pertence ao seu pedido.'])
        self.assertEqual(Avaliacao.objects.count(), 1)

    def _postar(self, item, nota):
        return self.client.post('/api/v1/avaliacoes/', {'pedido_produto': item.pedido_produto_id, 'nota': nota}, format='json')

    def _criar_produto(self, nome, sku, loja=None):
        return Produto.objects.create(loja=loja or self.produto.loja, nome=nome, estoque=10, sku=sku, categoria=self.produto.categoria)

    def _criar_item(self, usuario, nome_status, produto=None):
        produto = produto or self.produto
        status_pedido, _ = StatusPedido.objects.get_or_create(status=nome_status)
        pedido = Pedido.objects.create(loja=produto.loja, status=status_pedido)
        PedidoCliente.objects.create(
            pedido=pedido,
            usuario=usuario,
            nome=usuario.nome,
            cpf=usuario.cpf,
            email=usuario.email,
            data_nascimento=usuario.data_nascimento,
            genero=str(self.genero),
        )
        return PedidoProduto.objects.create(
            pedido=pedido,
            produto=produto,
            nome_produto=produto.nome,
            quantidade=1,
            valor_unitario=Decimal('5.00'),
            subtotal=Decimal('5.00'),
        )

    def _avaliar(self):
        return Avaliacao.objects.create(
            usuario=self.cliente,
            produto=self.produto,
            pedido_produto=self.item,
            nota=5,
            comentario='Muito bom',
        )

    def _criar_administrador(self):
        return Usuario.objects.create_superuser(
            cpf='32345678909',
            email='admin-avaliacao@example.com',
            password='senha123',
            nome='Administrador',
            data_nascimento='1985-01-01',
            genero=self.genero,
        )

    def _criar_usuario(self, cpf, email, **extras):
        return Usuario.objects.create_user(
            cpf=cpf,
            email=email,
            password='senha123',
            nome=f'Usuário {cpf}',
            data_nascimento='1990-01-01',
            genero=self.genero,
            **extras,
        )
