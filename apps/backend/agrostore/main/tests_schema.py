from django.apps import apps
from django.db import connection
from django.test import TestCase

DATAS = ['data_criacao', 'data_atualizacao']

MODELO_LOGICO = {
    'genero': ['codigo_genero', 'nome'],
    'usuario': [
        'id_usuario', 'nome', 'cpf', 'email', 'data_nascimento', 'foto_perfil', 'senha', 'ultimo_login',
        'e_produtor', 'esta_ativo', 'e_equipe', 'e_superusuario', 'codigo_genero',
    ],
    'redefinicao_senha': ['id_redefinicao', 'id_usuario', 'token_hash', 'data_expiracao', 'data_utilizacao', 'data_criacao'],
    'tipo_telefone': ['id_tipo_telefone', 'descricao'],
    'telefone': ['id_telefone', 'id_usuario', 'id_tipo_telefone', 'numero', 'e_principal'] + DATAS,
    'loja': ['id_loja', 'id_proprietario', 'nome', 'descricao', 'cnpj', 'imagem_perfil', 'esta_ativa'] + DATAS,
    'categoria': ['id_categoria', 'nome', 'esta_ativa'] + DATAS,
    'produto': [
        'id_produto', 'id_loja', 'id_categoria', 'nome', 'descricao', 'codigo_barras', 'estoque', 'sku', 'esta_ativo',
    ] + DATAS,
    'preco_produto': [
        'id_preco_produto', 'id_produto', 'valor_venda', 'valor_custo', 'valor_desconto', 'porcentagem_desconto',
        'vigencia_inicio', 'vigencia_fim',
    ] + DATAS,
    'imagem': ['id_imagem', 'id_produto', 'caminho', 'ordem', 'e_principal'] + DATAS,
    'carrinho': ['id_carrinho', 'id_usuario', 'id_loja', 'valor_bruto', 'valor_desconto', 'valor_liquido'] + DATAS,
    'carrinho_produto': ['id_carrinho_produto', 'id_carrinho', 'id_produto', 'quantidade'] + DATAS,
    'status_pedido': ['id_status_pedido', 'nome'],
    'pedido': ['id_pedido', 'id_loja', 'id_status_pedido', 'valor_bruto', 'valor_desconto', 'valor_liquido'] + DATAS,
    'pedido_cliente': [
        'id_pedido_cliente', 'id_pedido', 'id_usuario', 'nome', 'cpf', 'email', 'data_nascimento', 'genero',
    ] + DATAS,
    'pedido_produto': [
        'id_pedido_produto', 'id_pedido', 'id_produto', 'nome_produto', 'quantidade', 'valor_unitario',
        'valor_desconto', 'subtotal',
    ] + DATAS,
    'favorito': ['id_favorito', 'id_usuario', 'id_produto'] + DATAS,
    'avaliacao': ['id_avaliacao', 'id_usuario', 'id_produto', 'id_pedido_produto', 'nota', 'comentario'] + DATAS,
}

PK_BIGINT_EXCETO = {'genero'}


class SchemaModeloLogicoTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.cursor() as cursor:
            cls.tabelas = set(connection.introspection.table_names(cursor))
            cls.colunas = {
                tabela: [c.name for c in connection.introspection.get_table_description(cursor, tabela)]
                for tabela in MODELO_LOGICO if tabela in cls.tabelas
            }
            cls.pks = {
                tabela: connection.introspection.get_primary_key_columns(cursor, tabela)
                for tabela in MODELO_LOGICO if tabela in cls.tabelas
            }
        cls.models = {m._meta.db_table: m for m in apps.get_models()}

    def test_modelo_logico_tem_18_tabelas(self):
        self.assertEqual(len(MODELO_LOGICO), 18)

    def test_todas_as_tabelas_do_modelo_logico_existem(self):
        self.assertEqual(sorted(set(MODELO_LOGICO) - self.tabelas), [])

    def test_nao_ha_tabela_de_negocio_fora_do_modelo_logico(self):
        tecnicas = {'usuario_groups', 'usuario_user_permissions'}
        prefixos = ('django_', 'auth_')
        extras = {t for t in self.tabelas - set(MODELO_LOGICO) - tecnicas if not t.startswith(prefixos)}
        self.assertEqual(sorted(extras), [])

    def test_cada_tabela_tem_exatamente_as_colunas_do_modelo_logico(self):
        for tabela, esperadas in MODELO_LOGICO.items():
            with self.subTest(tabela=tabela):
                self.assertEqual(sorted(self.colunas[tabela]), sorted(esperadas))

    def test_chave_primaria_de_cada_tabela_tem_o_nome_do_modelo(self):
        for tabela, esperadas in MODELO_LOGICO.items():
            with self.subTest(tabela=tabela):
                self.assertEqual(self.pks[tabela], [esperadas[0]])

    def test_models_apontam_para_as_tabelas_do_modelo_logico(self):
        self.assertEqual(sorted(set(MODELO_LOGICO) - set(self.models)), [])

    def test_chaves_primarias_dos_models_sao_bigint_exceto_genero(self):
        for tabela in MODELO_LOGICO:
            if tabela in PK_BIGINT_EXCETO:
                continue
            with self.subTest(tabela=tabela):
                self.assertEqual(self.models[tabela]._meta.pk.get_internal_type(), 'BigAutoField')

    def test_genero_tem_chave_primaria_de_texto_com_2_caracteres(self):
        pk = self.models['genero']._meta.pk
        self.assertEqual(pk.get_internal_type(), 'CharField')
        self.assertEqual(pk.max_length, 2)

    def test_imagem_ordem_e_inteiro_positivo_e_caminho_tem_255_caracteres(self):
        modelo = self.models['imagem']
        campos = {campo.column: campo for campo in modelo._meta.get_fields() if hasattr(campo, 'column')}
        self.assertEqual(campos['ordem'].get_internal_type(), 'PositiveIntegerField')
        self.assertEqual(campos['caminho'].max_length, 255)

    def test_produto_nao_tem_coluna_imagem(self):
        self.assertNotIn('imagem', self.colunas['produto'])
