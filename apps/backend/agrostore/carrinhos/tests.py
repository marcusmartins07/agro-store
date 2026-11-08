import shutil
import tempfile
from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import connection
from django.test import override_settings
from django.test.utils import CaptureQueriesContext
from rest_framework import status
from rest_framework.test import APITestCase

from agrostore.carrinhos.models import Carrinho, CarrinhoProduto
from agrostore.lojas.models import Loja
from agrostore.produtos.models import Categoria, ImagemProduto, PrecoProduto, Produto
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

    def test_itens_informam_estoque_e_disponibilidade(self):
        self.client.post('/api/v1/carrinhos/', {'produto': self.produto.produto_id, 'quantidade': 2}, format='json')

        item = self.client.get('/api/v1/carrinhos/').data[0]['itens'][0]
        self.assertEqual(item['estoque'], 10)
        self.assertTrue(item['disponivel'])

        Produto.objects.filter(pk=self.produto.pk).update(estoque=0)
        item = self.client.get('/api/v1/carrinhos/').data[0]['itens'][0]
        self.assertEqual(item['estoque'], 0)
        self.assertFalse(item['disponivel'])

        Produto.objects.filter(pk=self.produto.pk).update(estoque=10)
        self.loja.ativa = False
        self.loja.save(update_fields=['ativa'])
        item = self.client.get('/api/v1/carrinhos/').data[0]['itens'][0]
        self.assertFalse(item['disponivel'])

    def test_rejeita_atualizar_item_para_quantidade_zero(self):
        self.client.post('/api/v1/carrinhos/', {'produto': self.produto.produto_id, 'quantidade': 2}, format='json')
        item = CarrinhoProduto.objects.get()

        response = self.client.patch(f'/api/v1/carrinhos/itens/{item.carrinho_produto_id}/', {'quantidade': 0}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        item.refresh_from_db()
        self.assertEqual(item.quantidade, 2)

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

    def _adicionar_item_com_quantidade(self, quantidade):
        carrinho = Carrinho.objects.create(usuario=self.cliente, loja=self.loja)
        item = CarrinhoProduto.objects.create(carrinho=carrinho, produto=self.produto, quantidade=quantidade)
        carrinho.recalcular_totais()
        return item

    def _url_item(self, item):
        return f'/api/v1/carrinhos/itens/{item.carrinho_produto_id}/'

    def test_rejeita_atualizar_item_acima_do_estoque(self):
        item = self._adicionar_item_com_quantidade(2)

        response = self.client.patch(self._url_item(item), {'quantidade': 11}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        item.refresh_from_db()
        self.assertEqual(item.quantidade, 2)

    def test_aceita_atualizar_item_ate_o_estoque(self):
        item = self._adicionar_item_com_quantidade(2)

        response = self.client.patch(self._url_item(item), {'quantidade': 10}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        self.assertEqual(item.quantidade, 10)

    def test_rejeita_adicionar_produto_sem_estoque(self):
        Produto.objects.filter(pk=self.produto.pk).update(estoque=0)

        response = self.client.post('/api/v1/carrinhos/', {'produto': self.produto.produto_id, 'quantidade': 1}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(CarrinhoProduto.objects.exists())

    def test_item_zerado_permanece_listado_com_totais_zerados_e_indisponivel(self):
        item = self._adicionar_item_com_quantidade(0)
        Produto.objects.filter(pk=self.produto.pk).update(estoque=0)

        response = self.client.get('/api/v1/carrinhos/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        item_resposta = response.data[0]['itens'][0]
        self.assertEqual(item_resposta['carrinho_produto_id'], item.carrinho_produto_id)
        self.assertEqual((item_resposta['quantidade'], item_resposta['estoque'], item_resposta['disponivel']), (0, 0, False))
        self.assertEqual(Decimal(response.data[0]['valor_liquido']), Decimal('0.00'))

    def test_rejeita_subir_item_zerado_enquanto_o_produto_continua_sem_estoque(self):
        item = self._adicionar_item_com_quantidade(0)
        Produto.objects.filter(pk=self.produto.pk).update(estoque=0)

        response = self.client.patch(self._url_item(item), {'quantidade': 1}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        item.refresh_from_db()
        self.assertEqual(item.quantidade, 0)

    def test_cliente_sobe_item_zerado_para_um_depois_da_reposicao_e_totais_voltam(self):
        item = self._adicionar_item_com_quantidade(0)
        Produto.objects.filter(pk=self.produto.pk).update(estoque=3)

        response = self.client.patch(self._url_item(item), {'quantidade': 1}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantidade'], 1)
        self.assertTrue(response.data['disponivel'])
        carrinho = Carrinho.objects.get(pk=item.carrinho_id)
        self.assertEqual(carrinho.valor_bruto, Decimal('10.00'))
        self.assertEqual(carrinho.valor_liquido, Decimal('8.00'))

    def test_adicionar_produto_repetido_soma_sobre_item_zerado_apos_reposicao(self):
        item = self._adicionar_item_com_quantidade(0)

        response = self.client.post('/api/v1/carrinhos/', {'produto': self.produto.produto_id, 'quantidade': 3}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        item.refresh_from_db()
        self.assertEqual(item.quantidade, 3)
        self.assertEqual(CarrinhoProduto.objects.count(), 1)

    def test_cliente_remove_item_zerado_e_carrinho_vazio_e_excluido(self):
        item = self._adicionar_item_com_quantidade(0)
        Produto.objects.filter(pk=self.produto.pk).update(estoque=0)

        response = self.client.delete(self._url_item(item))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CarrinhoProduto.objects.exists())
        self.assertFalse(Carrinho.objects.filter(usuario=self.cliente).exists())

    def test_item_de_produto_inativo_com_estoque_fica_indisponivel_mas_expoe_estoque(self):
        self._adicionar_item_com_quantidade(2)
        Produto.objects.filter(pk=self.produto.pk).update(ativo=False)

        item = self.client.get('/api/v1/carrinhos/').data[0]['itens'][0]

        self.assertEqual(item['estoque'], 10)
        self.assertFalse(item['disponivel'])

    def _criar_outra_loja(self):
        outro_produtor = Usuario.objects.create_user(
            cpf='12345678904',
            email='outro-produtor-carrinho@example.com',
            password='senha123',
            nome='Outro Produtor Teste',
            data_nascimento='1981-01-01',
            genero=self.genero,
            is_produtor=True,
        )
        return Loja.objects.create(proprietario=outro_produtor, nome='Loja Azul', cnpj='12345678000188')

    def test_rejeita_patch_da_loja_do_carrinho(self):
        item = self._adicionar_item_com_quantidade(2)
        outra_loja = self._criar_outra_loja()

        response = self.client.patch(f'/api/v1/carrinhos/{item.carrinho_id}/', {'loja': outra_loja.loja_id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Carrinho.objects.get(pk=item.carrinho_id).loja_id, self.loja.loja_id)

    def test_rejeita_patch_para_loja_onde_cliente_ja_tem_carrinho(self):
        item = self._adicionar_item_com_quantidade(2)
        outra_loja = self._criar_outra_loja()
        carrinho_destino = Carrinho.objects.create(usuario=self.cliente, loja=outra_loja)

        response = self.client.patch(f'/api/v1/carrinhos/{item.carrinho_id}/', {'loja': outra_loja.loja_id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Carrinho.objects.get(pk=item.carrinho_id).loja_id, self.loja.loja_id)
        self.assertEqual(Carrinho.objects.get(pk=carrinho_destino.pk).loja_id, outra_loja.loja_id)
        self.assertEqual(Carrinho.objects.filter(usuario=self.cliente).count(), 2)

    def test_rejeita_put_no_carrinho(self):
        item = self._adicionar_item_com_quantidade(2)

        response = self.client.put(f'/api/v1/carrinhos/{item.carrinho_id}/', {'loja': self.loja.loja_id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(CarrinhoProduto.objects.get(pk=item.pk).quantidade, 2)

    def test_rejeita_delete_do_carrinho(self):
        item = self._adicionar_item_com_quantidade(2)

        response = self.client.delete(f'/api/v1/carrinhos/{item.carrinho_id}/')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(Carrinho.objects.filter(pk=item.carrinho_id).exists())
        self.assertTrue(CarrinhoProduto.objects.filter(pk=item.pk).exists())

    def test_detalhe_do_carrinho_continua_acessivel_por_get(self):
        item = self._adicionar_item_com_quantidade(2)

        response = self.client.get(f'/api/v1/carrinhos/{item.carrinho_id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['loja'], self.loja.loja_id)


MEDIA_ROOT_TESTES = tempfile.mkdtemp()
PNG_VALIDO = b'\x89PNG\r\n\x1a\n' + b'\x00' * 32


@override_settings(MEDIA_ROOT=MEDIA_ROOT_TESTES)
class CarrinhoImagemProdutoAPITests(APITestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT_TESTES, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        genero, _ = Genero.objects.get_or_create(id_genero='M', defaults={'genero': 'Masculino'})
        self.cliente = Usuario.objects.create_user(
            cpf='12345678901',
            email='cliente@example.com',
            password='senha123',
            nome='Cliente Teste',
            data_nascimento='1990-01-01',
            genero=genero,
        )
        produtor = Usuario.objects.create_user(
            cpf='12345678903',
            email='produtor@example.com',
            password='senha123',
            nome='Produtor Teste',
            data_nascimento='1980-01-01',
            genero=genero,
            is_produtor=True,
        )
        self.loja = Loja.objects.create(proprietario=produtor, nome='Loja Verde', cnpj='12345678000199')
        self.categoria = Categoria.objects.create(nome='Frutas')
        self.produto = self.criar_produto('Maçã')
        self.client.force_authenticate(self.cliente)

    def criar_produto(self, nome):
        produto = Produto.objects.create(loja=self.loja, nome=nome, estoque=10, categoria=self.categoria)
        PrecoProduto.objects.create(produto=produto, preco_venda=Decimal('10.00'))
        return produto

    def criar_imagem(self, produto, ordem, e_principal):
        arquivo = SimpleUploadedFile(f'imagem{ordem}.png', PNG_VALIDO, content_type='image/png')
        return ImagemProduto.objects.create(produto=produto, imagem=arquivo, ordem=ordem, e_principal=e_principal)

    def url_absoluta(self, imagem):
        return f'http://testserver{imagem.imagem.url}'

    def test_listagem_retorna_url_absoluta_da_imagem_principal(self):
        self.criar_imagem(self.produto, 0, False)
        principal = self.criar_imagem(self.produto, 1, True)
        self.client.post('/api/v1/carrinhos/', {'produto': self.produto.produto_id, 'quantidade': 1}, format='json')

        response = self.client.get('/api/v1/carrinhos/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['itens'][0]['produto_imagem'], self.url_absoluta(principal))

    def test_produto_sem_imagem_retorna_nulo(self):
        self.client.post('/api/v1/carrinhos/', {'produto': self.produto.produto_id, 'quantidade': 1}, format='json')

        response = self.client.get('/api/v1/carrinhos/')

        self.assertIsNone(response.data[0]['itens'][0]['produto_imagem'])

    def test_adicionar_retorna_url_absoluta_da_imagem(self):
        principal = self.criar_imagem(self.produto, 0, True)

        novo = self.client.post('/api/v1/carrinhos/', {'produto': self.produto.produto_id, 'quantidade': 1}, format='json')
        repetido = self.client.post('/api/v1/carrinhos/', {'produto': self.produto.produto_id, 'quantidade': 1}, format='json')

        self.assertEqual(novo.status_code, status.HTTP_201_CREATED)
        self.assertEqual(novo.data['produto_imagem'], self.url_absoluta(principal))
        self.assertEqual(repetido.status_code, status.HTTP_201_CREATED)
        self.assertEqual(repetido.data['produto_imagem'], self.url_absoluta(principal))

    def test_atualizar_quantidade_retorna_url_absoluta_da_imagem(self):
        principal = self.criar_imagem(self.produto, 0, True)
        item_id = self.client.post(
            '/api/v1/carrinhos/', {'produto': self.produto.produto_id, 'quantidade': 1}, format='json'
        ).data['carrinho_produto_id']

        response = self.client.patch(f'/api/v1/carrinhos/itens/{item_id}/', {'quantidade': 3}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['produto_imagem'], self.url_absoluta(principal))

    def test_listagem_busca_imagens_em_uma_unica_consulta(self):
        outro_produto = self.criar_produto('Pera')
        for produto in (self.produto, outro_produto):
            self.criar_imagem(produto, 0, True)
            self.criar_imagem(produto, 1, False)
            self.client.post('/api/v1/carrinhos/', {'produto': produto.produto_id, 'quantidade': 1}, format='json')

        with CaptureQueriesContext(connection) as consultas:
            response = self.client.get('/api/v1/carrinhos/')

        consultas_de_imagem = [consulta for consulta in consultas.captured_queries if 'FROM "imagem"' in consulta['sql']]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[0]['itens']), 2)
        self.assertEqual(len(consultas_de_imagem), 1)

    def test_produto_imagem_enviada_no_post_e_no_patch_e_ignorada(self):
        principal = self.criar_imagem(self.produto, 0, True)
        falsa = 'http://exemplo.com/falsa.png'

        criado = self.client.post(
            '/api/v1/carrinhos/', {'produto': self.produto.produto_id, 'quantidade': 1, 'produto_imagem': falsa}, format='json'
        )
        item_id = criado.data['carrinho_produto_id']
        atualizado = self.client.patch(
            f'/api/v1/carrinhos/itens/{item_id}/', {'quantidade': 2, 'produto_imagem': falsa}, format='json'
        )

        self.assertEqual(criado.status_code, status.HTTP_201_CREATED)
        self.assertEqual(criado.data['produto_imagem'], self.url_absoluta(principal))
        self.assertEqual(atualizado.status_code, status.HTTP_200_OK)
        self.assertEqual(atualizado.data['produto_imagem'], self.url_absoluta(principal))
        self.assertEqual(CarrinhoProduto.objects.get(pk=item_id).quantidade, 2)
