from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase

ANTES = ('produtos', '0007_nomes_fisicos_modelo_logico')
ATUAL = ('produtos', '0008_remove_produto_imagem')
CAMINHO = 'produtos/migracao-legada.jpg'
OUTRO_CAMINHO = 'produtos/migracao-outra.jpg'


class MigracaoRemocaoImagemLegadaTests(TransactionTestCase):

    def setUp(self):
        self.apps_antes = self._migrar(ANTES)
        self.produto_id = self._criar_produto(CAMINHO)

    def tearDown(self):
        if 'imagem' in self._colunas_produto():
            with connection.cursor() as cursor:
                cursor.execute("UPDATE produto SET imagem = ''")
        self._migrar_para_folhas()
        from agrostore.lojas.models import Loja
        from agrostore.produtos.models import Categoria
        from agrostore.usuarios.models import Genero, Usuario
        Loja.objects.filter(cnpj='42345678000188').delete()
        Categoria.objects.filter(nome='Categoria Migração').delete()
        Usuario.objects.filter(email='produtor@migracao.test').delete()
        Genero.objects.filter(id_genero='Z').delete()

    def test_migration_e_interrompida_quando_imagem_legada_nao_tem_imagem_correspondente(self):
        self._criar_imagem(self.produto_id, OUTRO_CAMINHO)

        with self.assertRaises(RuntimeError) as contexto:
            self._migrar(ATUAL)

        self.assertIn('DB-019 interrompida', str(contexto.exception))
        self.assertIn('imagem', self._colunas_produto())
        self.assertEqual(self._imagem_legada(), CAMINHO)

    def test_migration_remove_a_coluna_quando_ha_imagem_correspondente(self):
        self._criar_imagem(self.produto_id, CAMINHO)

        self._migrar(ATUAL)

        self.assertNotIn('imagem', self._colunas_produto())

    def test_reversao_recopia_o_caminho_da_imagem_principal_para_o_produto(self):
        self._criar_imagem(self.produto_id, CAMINHO, ordem=0, principal=False)
        self._criar_imagem(self.produto_id, OUTRO_CAMINHO, ordem=1, principal=True)
        self._migrar(ATUAL)

        self._migrar(ANTES)

        self.assertIn('imagem', self._colunas_produto())
        self.assertEqual(self._imagem_legada(), OUTRO_CAMINHO)

    def _criar_produto(self, caminho):
        genero_model = self.apps_antes.get_model('usuarios', 'Genero')
        usuario_model = self.apps_antes.get_model('usuarios', 'Usuario')
        loja_model = self.apps_antes.get_model('lojas', 'Loja')
        categoria_model = self.apps_antes.get_model('produtos', 'Categoria')
        produto_model = self.apps_antes.get_model('produtos', 'Produto')
        genero, _ = genero_model.objects.get_or_create(id_genero='Z', defaults={'genero': 'Teste Migração'})
        produtor = usuario_model.objects.create(
            cpf='42345678911', email='produtor@migracao.test', nome='Produtor', data_nascimento='1980-01-01',
            genero=genero, password='x', foto_perfil='',
        )
        loja = loja_model.objects.create(proprietario=produtor, nome='Loja Migração', cnpj='42345678000188')
        categoria = categoria_model.objects.create(nome='Categoria Migração')
        produto = produto_model.objects.create(loja=loja, categoria=categoria, nome='Produto Migração', imagem=caminho)
        return produto.pk

    def _criar_imagem(self, produto_id, caminho, ordem=0, principal=True):
        imagem_model = self.apps_antes.get_model('produtos', 'ImagemProduto')
        imagem_model.objects.create(produto_id=produto_id, imagem=caminho, ordem=ordem, e_principal=principal)

    def _colunas_produto(self):
        with connection.cursor() as cursor:
            descricao = connection.introspection.get_table_description(cursor, 'produto')
        return [coluna.name for coluna in descricao]

    def _imagem_legada(self):
        with connection.cursor() as cursor:
            cursor.execute('SELECT imagem FROM produto WHERE id_produto = %s', [self.produto_id])
            return cursor.fetchone()[0]

    def _migrar_para_folhas(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())

    def _migrar(self, alvo):
        executor = MigrationExecutor(connection)
        folhas = [no for no in executor.loader.graph.leaf_nodes() if no[0] != 'produtos']
        alvos = folhas + [alvo]
        executor.migrate(alvos)
        executor = MigrationExecutor(connection)
        return executor.loader.project_state(alvos).apps
