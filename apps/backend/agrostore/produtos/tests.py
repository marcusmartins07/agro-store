import shutil
import tempfile
from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.db.models.deletion import ProtectedError
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from agrostore.carrinhos.models import Carrinho, CarrinhoProduto
from agrostore.lojas.models import Loja
from agrostore.produtos.models import Categoria, ImagemProduto, PrecoProduto, Produto
from agrostore.produtos.serializers import TAMANHO_MAXIMO_IMAGEM_PRODUTO, ProdutoSerializer
from agrostore.produtos.views import ProdutoViewSet
from agrostore.usuarios.models import Genero, Usuario


class ProdutoCategoriaAPITests(APITestCase):
    def setUp(self):
        self.genero, _ = Genero.objects.get_or_create(id_genero='M', defaults={'genero': 'Masculino'})
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

    def test_criacao_gera_sku_com_ids_preenchidos_por_zeros(self):
        self.client.force_authenticate(self.produtor)

        response = self.client.post(
            '/api/v1/produtos/',
            self.produto_payload(sku='SKU-MANUAL-IGNORADO'),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        sku_esperado = f'{self.loja.loja_id:04d}{self.categoria_ativa.categoria_id:04d}{response.data["produto_id"]:06d}'
        self.assertEqual(response.data['sku'], sku_esperado)

    def test_sku_permanece_inalterado_apos_edicao(self):
        sku_original = self.produto.sku
        self.produto.categoria = self.categoria_inativa
        self.produto.save(update_fields=['categoria'])
        self.produto.refresh_from_db()

        self.assertEqual(self.produto.sku, sku_original)

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

    def test_cliente_nao_pode_cadastrar_produto(self):
        self.client.force_authenticate(self.cliente)

        response = self.client.post('/api/v1/produtos/', self.produto_payload(), format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_produtor_lista_apenas_os_proprios_produtos(self):
        outro_produtor = self.criar_usuario('12345678904', 'outro-produtor@example.com', is_produtor=True)
        outra_loja = Loja.objects.create(proprietario=outro_produtor, nome='Outra Feira', cnpj='12345678000198')
        produto_outro = Produto.objects.create(
            loja=outra_loja,
            nome='Tomate',
            sku='TOMATE-001',
            estoque=8,
            categoria=self.categoria_ativa,
        )
        self.client.force_authenticate(self.produtor)

        response = self.client.get('/api/v1/produtos/meus/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([produto['produto_id'] for produto in response.data], [self.produto.produto_id])
        self.assertNotIn(produto_outro.produto_id, [produto['produto_id'] for produto in response.data])

    def test_produtor_nao_edita_produto_de_outra_loja(self):
        outro_produtor = self.criar_usuario('12345678904', 'outro-produtor@example.com', is_produtor=True)
        outra_loja = Loja.objects.create(proprietario=outro_produtor, nome='Outra Feira', cnpj='12345678000198')
        produto_outro = Produto.objects.create(
            loja=outra_loja,
            nome='Tomate',
            sku='TOMATE-001',
            estoque=8,
            categoria=self.categoria_ativa,
        )
        self.client.force_authenticate(self.produtor)

        response = self.client.patch(
            f'/api/v1/produtos/{produto_outro.produto_id}/',
            {'estoque': 1},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_produtor_cria_preco_apenas_para_produto_proprio(self):
        self.client.force_authenticate(self.produtor)
        PrecoProduto.objects.create(produto=self.produto, preco_venda='10.00')

        response = self.client.post(
            '/api/v1/produtos/precos/',
            {'produto': self.produto.produto_id, 'preco_venda': '12.00', 'porcentagem_desconto': 10},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PrecoProduto.objects.filter(produto=self.produto, vigencia_fim__isnull=True).count(), 1)

    def _postar_preco(self, **campos):
        self.client.force_authenticate(self.produtor)
        return self.client.post('/api/v1/produtos/precos/', {'produto': self.produto.produto_id, **campos}, format='json')

    def test_preco_de_venda_negativo_e_recusado_com_mensagem(self):
        response = self._postar_preco(preco_venda='-0.01')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['preco_venda'], ['O preço de venda não pode ser negativo.'])
        self.assertFalse(PrecoProduto.objects.exists())

    def test_preco_de_custo_negativo_e_recusado_com_mensagem(self):
        response = self._postar_preco(preco_venda='10.00', preco_custo='-1.00')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['preco_custo'], ['O preço de custo não pode ser negativo.'])
        self.assertFalse(PrecoProduto.objects.exists())

    def test_precos_zerados_sao_aceitos(self):
        response = self._postar_preco(preco_venda='0.00', preco_custo='0.00')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        preco = PrecoProduto.objects.get()
        self.assertEqual((preco.preco_venda, preco.preco_custo), (Decimal('0.00'), Decimal('0.00')))

    def test_preco_de_custo_nulo_ou_ausente_e_aceito(self):
        nulo = self._postar_preco(preco_venda='10.00', preco_custo=None)
        ausente = self._postar_preco(preco_venda='11.00')

        self.assertEqual((nulo.status_code, ausente.status_code), (status.HTTP_201_CREATED, status.HTTP_201_CREATED))
        self.assertIsNone(PrecoProduto.objects.get(preco_venda=Decimal('11.00')).preco_custo)


class ProdutoEstoqueAPITests(APITestCase):
    def setUp(self):
        genero, _ = Genero.objects.get_or_create(id_genero='M', defaults={'genero': 'Masculino'})
        self.produtor = Usuario.objects.create_user(
            cpf='32345678901',
            email='produtor-estoque@example.com',
            password='senha123',
            nome='Produtor Estoque',
            data_nascimento='1980-01-01',
            genero=genero,
            is_produtor=True,
        )
        self.clientes = [
            Usuario.objects.create_user(
                cpf=f'3234567890{indice}',
                email=f'cliente-estoque-{indice}@example.com',
                password='senha123',
                nome=f'Cliente Estoque {indice}',
                data_nascimento='1990-01-01',
                genero=genero,
            )
            for indice in (2, 3)
        ]
        self.loja = Loja.objects.create(proprietario=self.produtor, nome='Feira Estoque', cnpj='32345678000199')
        self.categoria = Categoria.objects.create(nome='Frutas')
        self.produto = Produto.objects.create(loja=self.loja, nome='Maçã', estoque=10, categoria=self.categoria)
        PrecoProduto.objects.create(produto=self.produto, preco_venda=Decimal('10.00'), preco_desconto=Decimal('2.00'))
        self.url_produto = f'/api/v1/produtos/{self.produto.produto_id}/'

    def adicionar_item(self, cliente, quantidade):
        carrinho, _ = Carrinho.objects.get_or_create(usuario=cliente, loja=self.loja)
        item = CarrinhoProduto.objects.create(carrinho=carrinho, produto=self.produto, quantidade=quantidade)
        carrinho.recalcular_totais()
        return item

    def alterar_estoque(self, estoque):
        self.client.force_authenticate(self.produtor)
        return self.client.patch(self.url_produto, {'estoque': estoque}, format='json')

    def test_listagem_omite_produto_sem_estoque_mas_detalhe_e_meus_continuam_acessiveis(self):
        Produto.objects.filter(pk=self.produto.pk).update(estoque=0)

        listagem = self.client.get('/api/v1/produtos/')
        detalhe = self.client.get(self.url_produto)
        self.client.force_authenticate(self.produtor)
        meus = self.client.get('/api/v1/produtos/meus/')

        self.assertEqual(listagem.data, [])
        self.assertEqual(detalhe.status_code, status.HTTP_200_OK)
        self.assertEqual(detalhe.data['estoque'], 0)
        self.assertEqual([produto['produto_id'] for produto in meus.data], [self.produto.produto_id])

        self.alterar_estoque(3)
        self.client.force_authenticate(None)
        listagem = self.client.get('/api/v1/produtos/')
        self.assertEqual([produto['produto_id'] for produto in listagem.data], [self.produto.produto_id])

    def test_estoque_baixo_considera_de_um_ate_o_limite(self):
        casos = {0: False, 1: True, Produto.LIMITE_ESTOQUE_BAIXO: True, Produto.LIMITE_ESTOQUE_BAIXO + 1: False}

        for estoque, esperado in casos.items():
            Produto.objects.filter(pk=self.produto.pk).update(estoque=estoque)
            response = self.client.get(self.url_produto)
            self.assertIs(response.data['estoque_baixo'], esperado, f'estoque={estoque}')

    def test_estoque_negativo_e_rejeitado(self):
        self.client.force_authenticate(self.produtor)

        criacao = self.client.post(
            '/api/v1/produtos/',
            {'nome': 'Pera', 'estoque': -1, 'categoria': self.categoria.categoria_id},
            format='json',
        )
        edicao = self.alterar_estoque(-1)

        self.assertEqual(criacao.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('estoque', criacao.data)
        self.assertEqual(edicao.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('estoque', edicao.data)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoque, 10)

    def test_reducao_de_estoque_ajusta_carrinhos_acima_do_novo_estoque(self):
        item_acima = self.adicionar_item(self.clientes[0], 8)
        item_abaixo = self.adicionar_item(self.clientes[1], 3)
        atualizado_antes = item_acima.data_atualizacao

        response = self.alterar_estoque(5)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item_acima.refresh_from_db()
        item_abaixo.refresh_from_db()
        self.assertEqual(item_acima.quantidade, 5)
        self.assertGreater(item_acima.data_atualizacao, atualizado_antes)
        self.assertEqual(item_abaixo.quantidade, 3)
        self.assertEqual(item_acima.carrinho.valor_bruto, Decimal('50.00'))
        self.assertEqual(item_acima.carrinho.valor_liquido, Decimal('40.00'))

    def test_estoque_zerado_mantem_itens_com_quantidade_zero_e_reposicao_nao_restaura(self):
        item = self.adicionar_item(self.clientes[0], 4)

        self.alterar_estoque(0)
        item.refresh_from_db()
        self.assertEqual(item.quantidade, 0)
        self.assertEqual(item.carrinho.valor_liquido, Decimal('0.00'))
        self.assertTrue(Carrinho.objects.filter(pk=item.carrinho_id).exists())

        self.alterar_estoque(10)
        item.refresh_from_db()
        self.assertEqual(item.quantidade, 0)

    def test_edicao_sem_estoque_nao_altera_carrinhos(self):
        item = self.adicionar_item(self.clientes[0], 8)
        Produto.objects.filter(pk=self.produto.pk).update(estoque=2)
        self.client.force_authenticate(self.produtor)

        response = self.client.patch(self.url_produto, {'nome': 'Maçã gala'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['estoque'], 2)
        item.refresh_from_db()
        self.assertEqual(item.quantidade, 8)

    def test_edicao_sem_estoque_preserva_baixa_feita_depois_da_leitura_do_produto(self):
        produto_lido_pela_view = Produto.objects.get(pk=self.produto.pk)
        Produto.objects.filter(pk=self.produto.pk).update(estoque=3)
        serializer = ProdutoSerializer(produto_lido_pela_view, data={'nome': 'Maçã gala'}, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        ProdutoViewSet().perform_update(serializer)

        self.produto.refresh_from_db()
        self.assertEqual(self.produto.nome, 'Maçã gala')
        self.assertEqual(self.produto.estoque, 3)

    def criar_cliente(self, indice):
        genero = Genero.objects.get(id_genero='M')
        return Usuario.objects.create_user(
            cpf=f'3234567891{indice}',
            email=f'cliente-estoque-extra-{indice}@example.com',
            password='senha123',
            nome=f'Cliente Extra {indice}',
            data_nascimento='1990-01-01',
            genero=genero,
        )

    def criar_produto(self, nome, estoque):
        produto = Produto.objects.create(loja=self.loja, nome=nome, estoque=estoque, categoria=self.categoria)
        PrecoProduto.objects.create(produto=produto, preco_venda=Decimal('5.00'), preco_desconto=Decimal('0.00'))
        return produto

    def test_listagem_oculta_so_o_produto_zerado_sem_desativa_lo_e_ele_volta_na_reposicao(self):
        pera = self.criar_produto('Pera', 4)

        self.alterar_estoque(0)
        self.client.force_authenticate(None)
        listagem = self.client.get('/api/v1/produtos/')
        filtrada = self.client.get(f'/api/v1/produtos/?categoria={self.categoria.categoria_id}')

        self.assertEqual([produto['produto_id'] for produto in listagem.data], [pera.produto_id])
        self.assertEqual([produto['produto_id'] for produto in filtrada.data], [pera.produto_id])
        self.produto.refresh_from_db()
        self.assertTrue(self.produto.ativo)

        self.alterar_estoque(1)
        self.client.force_authenticate(None)
        listagem = self.client.get('/api/v1/produtos/')
        self.assertCountEqual([produto['produto_id'] for produto in listagem.data], [self.produto.produto_id, pera.produto_id])

    def test_estoque_baixo_aparece_na_listagem_e_em_meus_nos_limites(self):
        self.client.force_authenticate(self.produtor)
        casos = {1: True, Produto.LIMITE_ESTOQUE_BAIXO: True, Produto.LIMITE_ESTOQUE_BAIXO + 1: False}

        for estoque, esperado in casos.items():
            Produto.objects.filter(pk=self.produto.pk).update(estoque=estoque)
            listagem = self.client.get('/api/v1/produtos/').data[0]
            meus = self.client.get('/api/v1/produtos/meus/').data[0]
            self.assertIs(listagem['estoque_baixo'], esperado, f'listagem estoque={estoque}')
            self.assertIs(meus['estoque_baixo'], esperado, f'meus estoque={estoque}')

        Produto.objects.filter(pk=self.produto.pk).update(estoque=0)
        self.assertFalse(self.client.get('/api/v1/produtos/meus/').data[0]['estoque_baixo'])

    def test_estoque_negativo_retorna_mensagem_clara_sem_criar_nem_alterar_dados(self):
        item = self.adicionar_item(self.clientes[0], 8)
        self.client.force_authenticate(self.produtor)

        criacao = self.client.post(
            '/api/v1/produtos/',
            {'nome': 'Pera', 'estoque': -5, 'categoria': self.categoria.categoria_id},
            format='json',
        )
        edicao = self.client.patch(self.url_produto, {'nome': 'Maçã gala', 'estoque': -1}, format='json')

        self.assertEqual(criacao.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(criacao.data, {'estoque': ['O estoque não pode ser negativo.']})
        self.assertEqual(edicao.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(edicao.data, {'estoque': ['O estoque não pode ser negativo.']})
        self.assertFalse(Produto.objects.filter(nome='Pera').exists())
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoque, 10)
        self.assertEqual(self.produto.nome, 'Maçã')
        item.refresh_from_db()
        self.assertEqual(item.quantidade, 8)

    def test_estoque_zero_e_aceito_no_cadastro_e_na_edicao(self):
        self.client.force_authenticate(self.produtor)

        criacao = self.client.post(
            '/api/v1/produtos/',
            {'nome': 'Pera', 'estoque': 0, 'categoria': self.categoria.categoria_id},
            format='json',
        )
        edicao = self.alterar_estoque(0)

        self.assertEqual(criacao.status_code, status.HTTP_201_CREATED)
        self.assertEqual(edicao.status_code, status.HTTP_200_OK)

    def test_reducao_ajusta_so_itens_acima_e_preserva_iguais_e_abaixo_com_totais(self):
        cliente_extra = self.criar_cliente(1)
        item_acima = self.adicionar_item(self.clientes[0], 8)
        item_igual = self.adicionar_item(self.clientes[1], 5)
        item_abaixo = self.adicionar_item(cliente_extra, 2)
        atualizado_igual = item_igual.data_atualizacao
        atualizado_abaixo = item_abaixo.data_atualizacao

        response = self.alterar_estoque(5)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in (item_acima, item_igual, item_abaixo):
            item.refresh_from_db()
        self.assertEqual([item_acima.quantidade, item_igual.quantidade, item_abaixo.quantidade], [5, 5, 2])
        self.assertEqual(item_igual.data_atualizacao, atualizado_igual)
        self.assertEqual(item_abaixo.data_atualizacao, atualizado_abaixo)
        esperado = {
            item_acima: (Decimal('50.00'), Decimal('40.00')),
            item_igual: (Decimal('50.00'), Decimal('40.00')),
            item_abaixo: (Decimal('20.00'), Decimal('16.00')),
        }
        for item, (bruto, liquido) in esperado.items():
            carrinho = Carrinho.objects.get(pk=item.carrinho_id)
            self.assertEqual((carrinho.valor_bruto, carrinho.valor_liquido), (bruto, liquido))

    def test_aumento_de_estoque_nao_restaura_quantidade_reduzida_nem_altera_totais(self):
        item = self.adicionar_item(self.clientes[0], 8)
        self.alterar_estoque(5)

        response = self.alterar_estoque(20)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        self.assertEqual(item.quantidade, 5)
        carrinho = Carrinho.objects.get(pk=item.carrinho_id)
        self.assertEqual(carrinho.valor_bruto, Decimal('50.00'))
        self.assertEqual(carrinho.valor_liquido, Decimal('40.00'))

    def test_ajuste_de_estoque_nao_afeta_itens_de_outro_produto(self):
        pera = self.criar_produto('Pera', 20)
        item_maca = self.adicionar_item(self.clientes[0], 8)
        item_pera = CarrinhoProduto.objects.create(carrinho=item_maca.carrinho, produto=pera, quantidade=9)

        self.alterar_estoque(1)

        item_pera.refresh_from_db()
        item_maca.refresh_from_db()
        self.assertEqual(item_pera.quantidade, 9)
        self.assertEqual(item_maca.quantidade, 1)

    def test_item_zerado_pelo_produtor_continua_no_carrinho_do_cliente_e_reposicao_o_torna_disponivel(self):
        self.adicionar_item(self.clientes[0], 4)
        self.alterar_estoque(0)
        self.client.force_authenticate(self.clientes[0])

        carrinhos = self.client.get('/api/v1/carrinhos/').data

        self.assertEqual(len(carrinhos), 1)
        item = carrinhos[0]['itens'][0]
        self.assertEqual((item['quantidade'], item['estoque'], item['disponivel']), (0, 0, False))
        self.assertEqual(Decimal(carrinhos[0]['valor_liquido']), Decimal('0.00'))

        self.alterar_estoque(10)
        self.client.force_authenticate(self.clientes[0])
        item = self.client.get('/api/v1/carrinhos/').data[0]['itens'][0]
        self.assertEqual((item['quantidade'], item['estoque'], item['disponivel']), (0, 10, True))


MEDIA_ROOT_TESTES = tempfile.mkdtemp()
PNG_VALIDO = b'\x89PNG\r\n\x1a\n' + b'\x00' * 32


@override_settings(MEDIA_ROOT=MEDIA_ROOT_TESTES)
class ProdutoImagemAPITests(APITestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT_TESTES, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        genero, _ = Genero.objects.get_or_create(id_genero='M', defaults={'genero': 'Masculino'})
        self.produtor = self.criar_usuario('12345678901', 'produtor@example.com', genero, is_produtor=True)
        self.outro_produtor = self.criar_usuario('12345678902', 'outro@example.com', genero, is_produtor=True)
        loja = Loja.objects.create(proprietario=self.produtor, nome='Feira Verde', cnpj='12345678000199')
        categoria = Categoria.objects.create(nome='Frutas')
        self.produto = Produto.objects.create(loja=loja, nome='Maçã', estoque=10, categoria=categoria)
        self.url_imagens = f'/api/v1/produtos/{self.produto.produto_id}/imagens/'

    def criar_usuario(self, cpf, email, genero, **extra_fields):
        return Usuario.objects.create_user(
            cpf=cpf,
            email=email,
            password='senha123',
            nome=email.split('@')[0],
            data_nascimento='1990-01-01',
            genero=genero,
            **extra_fields,
        )

    def enviar_imagem(self, nome_arquivo='maca.png', conteudo=PNG_VALIDO, usuario=None, **dados):
        self.client.force_authenticate(usuario or self.produtor)
        arquivo = SimpleUploadedFile(nome_arquivo, conteudo, content_type='image/png')
        return self.client.post(self.url_imagens, {'imagem': arquivo, **dados}, format='multipart')

    def url_imagem(self, imagem_id):
        return f'{self.url_imagens}{imagem_id}/'

    def test_primeira_imagem_vira_principal(self):
        response = self.enviar_imagem()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        imagem = ImagemProduto.objects.get(produto=self.produto)
        self.assertTrue(imagem.e_principal)
        self.assertEqual(imagem.ordem, 0)
        self.assertTrue(imagem.imagem.name.startswith('produtos/'))
        self.assertNotIn('maca', imagem.imagem.name)

    def test_catalogo_expoe_imagem_principal_e_lista_de_imagens(self):
        self.enviar_imagem()
        self.enviar_imagem()
        principal = ImagemProduto.objects.get(produto=self.produto, e_principal=True)

        response = self.client.get(f'/api/v1/produtos/{self.produto.produto_id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['imagem'].endswith(principal.imagem.name))
        self.assertEqual([imagem['ordem'] for imagem in response.data['imagens']], [0, 1])
        self.assertEqual([imagem['e_principal'] for imagem in response.data['imagens']], [True, False])

    def test_produto_sem_imagem_retorna_imagem_nula(self):
        response = self.client.get(f'/api/v1/produtos/{self.produto.produto_id}/')

        self.assertIsNone(response.data['imagem'])
        self.assertEqual(response.data['imagens'], [])

    def test_sexta_imagem_e_rejeitada(self):
        for _ in range(ImagemProduto.LIMITE_POR_PRODUTO):
            self.assertEqual(self.enviar_imagem().status_code, status.HTTP_201_CREATED)

        response = self.enviar_imagem()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('imagem', response.data)
        self.assertEqual(self.produto.imagens.count(), ImagemProduto.LIMITE_POR_PRODUTO)

    def test_imagem_com_conteudo_invalido_e_rejeitada(self):
        response = self.enviar_imagem(conteudo=b'nao sou uma imagem')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('imagem', response.data)

    def test_imagem_com_extensao_nao_permitida_e_rejeitada(self):
        response = self.enviar_imagem(nome_arquivo='maca.gif')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('imagem', response.data)

    def test_imagem_acima_do_limite_e_rejeitada(self):
        response = self.enviar_imagem(conteudo=PNG_VALIDO + b'\x00' * TAMANHO_MAXIMO_IMAGEM_PRODUTO)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('imagem', response.data)

    def test_outro_produtor_nao_gerencia_imagens(self):
        self.enviar_imagem()
        imagem = ImagemProduto.objects.get(produto=self.produto)

        envio = self.enviar_imagem(usuario=self.outro_produtor)
        exclusao = self.client.delete(self.url_imagem(imagem.id))

        self.assertEqual(envio.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(exclusao.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.produto.imagens.count(), 1)

    def test_visitante_nao_envia_imagem(self):
        arquivo = SimpleUploadedFile('maca.png', PNG_VALIDO, content_type='image/png')

        response = self.client.post(self.url_imagens, {'imagem': arquivo}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_leitura_segue_visibilidade_do_produto(self):
        self.enviar_imagem()
        self.client.force_authenticate(None)

        self.assertEqual(self.client.get(self.url_imagens).status_code, status.HTTP_200_OK)

        self.produto.ativo = False
        self.produto.save()
        self.assertEqual(self.client.get(self.url_imagens).status_code, status.HTTP_404_NOT_FOUND)

        self.client.force_authenticate(self.produtor)
        self.assertEqual(self.client.get(self.url_imagens).status_code, status.HTTP_200_OK)

    def test_definir_principal_desmarca_a_anterior(self):
        self.enviar_imagem()
        self.enviar_imagem()
        primeira, segunda = ImagemProduto.objects.filter(produto=self.produto)

        response = self.client.patch(self.url_imagem(segunda.id), {'e_principal': True}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        primeira.refresh_from_db()
        segunda.refresh_from_db()
        self.assertFalse(primeira.e_principal)
        self.assertTrue(segunda.e_principal)

    def test_envio_marcado_como_principal_desmarca_a_anterior(self):
        self.enviar_imagem()
        response = self.enviar_imagem(e_principal=True)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        principal = ImagemProduto.objects.get(produto=self.produto, e_principal=True)
        self.assertEqual(principal.id, response.data['id'])

    def test_principal_nao_pode_ser_desmarcada_diretamente(self):
        self.enviar_imagem()
        imagem = ImagemProduto.objects.get(produto=self.produto)

        response = self.client.patch(self.url_imagem(imagem.id), {'e_principal': False}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        imagem.refresh_from_db()
        self.assertTrue(imagem.e_principal)

    def test_arquivo_da_imagem_nao_pode_ser_trocado(self):
        self.enviar_imagem()
        imagem = ImagemProduto.objects.get(produto=self.produto)
        arquivo = SimpleUploadedFile('pera.png', PNG_VALIDO, content_type='image/png')

        response = self.client.patch(self.url_imagem(imagem.id), {'imagem': arquivo}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('imagem', response.data)

    def test_excluir_principal_promove_a_proxima_e_remove_arquivo(self):
        self.enviar_imagem()
        self.enviar_imagem()
        primeira, segunda = ImagemProduto.objects.filter(produto=self.produto)
        storage = primeira.imagem.storage
        arquivo_excluido = primeira.imagem.name

        response = self.client.delete(self.url_imagem(primeira.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        segunda.refresh_from_db()
        self.assertTrue(segunda.e_principal)
        self.assertFalse(storage.exists(arquivo_excluido))
        self.assertTrue(storage.exists(segunda.imagem.name))

    def test_reordenar_imagens(self):
        for _ in range(3):
            self.enviar_imagem()
        primeira, segunda, terceira = ImagemProduto.objects.filter(produto=self.produto)

        response = self.client.post(
            f'{self.url_imagens}reordenar/',
            {'imagens': [terceira.id, primeira.id, segunda.id]},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([imagem['id'] for imagem in response.data], [terceira.id, primeira.id, segunda.id])
        primeira.refresh_from_db()
        self.assertTrue(primeira.e_principal)

    def test_reordenar_exige_todas_as_imagens_do_produto(self):
        self.enviar_imagem()
        self.enviar_imagem()
        primeira = ImagemProduto.objects.filter(produto=self.produto).first()

        response = self.client.post(f'{self.url_imagens}reordenar/', {'imagens': [primeira.id]}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('imagens', response.data)

    def test_banco_impede_duas_imagens_principais(self):
        ImagemProduto.objects.create(produto=self.produto, imagem='produtos/a.png', e_principal=True)

        with self.assertRaises(IntegrityError):
            ImagemProduto.objects.create(produto=self.produto, imagem='produtos/b.png', ordem=1, e_principal=True)

    def test_edicao_do_produto_mantem_imagens(self):
        self.enviar_imagem()

        response = self.client.patch(f'/api/v1/produtos/{self.produto.produto_id}/', {'estoque': 3}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['imagens']), 1)
