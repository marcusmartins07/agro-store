import io
from contextlib import redirect_stdout

from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase

ANTES = [('usuarios', '0006_tipotelefone_telefone')]
ATUAL = [('usuarios', '0008_remove_usuario_telefone')]


class MigracaoTelefonesTests(TransactionTestCase):
    """DB-018: Usuario.telefone (0006, schema novo) passa a Telefone na 0007 e o campo antigo sai na 0008 (RN-021)."""

    def setUp(self):
        self.apps_antes = self._migrar(ANTES)

    def tearDown(self):
        # Volta ao estado final e remove os dados históricos para não afetar os demais testes.
        apps = self._migrar(ATUAL)
        apps.get_model('usuarios', 'Telefone').objects.all().delete()
        apps.get_model('usuarios', 'Usuario').objects.filter(email__endswith='@migracao.test').delete()
        apps.get_model('usuarios', 'Genero').objects.filter(id_genero='Z').delete()
        self._migrar_para_folhas()

    def test_copia_o_telefone_antigo_como_principal_com_o_tipo_pela_quantidade_de_digitos(self):
        casos = {'celular': '51999990000', 'fixo': '5133334444'}
        usuarios = {nome: self._criar_usuario(nome, numero) for nome, numero in casos.items()}

        apps = self._migrar(ATUAL)

        for nome, numero in casos.items():
            telefone = apps.get_model('usuarios', 'Telefone').objects.get(usuario_id=usuarios[nome])
            self.assertEqual(telefone.numero, numero)
            self.assertTrue(telefone.e_principal)
        self.assertEqual(self._telefone(apps, usuarios['celular']).tipo.descricao, 'Celular')
        self.assertEqual(self._telefone(apps, usuarios['fixo']).tipo.descricao, 'Fixo')

    def test_numero_fora_do_padrao_entra_como_celular_e_a_contagem_e_informada_sem_expor_o_numero(self):
        curto = self._criar_usuario('curto', '123456789')
        longo = self._criar_usuario('longo', '519999900001')

        saida = io.StringIO()
        with redirect_stdout(saida):
            apps = self._migrar(ATUAL)

        for usuario_id, numero in ((curto, '123456789'), (longo, '519999900001')):
            telefone = self._telefone(apps, usuario_id)
            self.assertEqual((telefone.tipo.descricao, telefone.numero, telefone.e_principal), ('Celular', numero, True))
        self.assertIn('2 telefone(s) fora do padrão', saida.getvalue())
        self.assertNotIn('123456789', saida.getvalue())
        self.assertNotIn('519999900001', saida.getvalue())

    def test_telefone_nulo_vazio_ou_sem_digitos_nao_gera_linha(self):
        for nome, numero in (('nulo', None), ('vazio', ''), ('letras', 'abc')):
            self._criar_usuario(nome, numero)

        apps = self._migrar(ATUAL)

        self.assertEqual(apps.get_model('usuarios', 'Telefone').objects.count(), 0)
        self.assertEqual(apps.get_model('usuarios', 'Usuario').objects.filter(email__endswith='@migracao.test').count(), 3)

    def test_cada_usuario_recebe_somente_um_telefone_principal(self):
        for indice in range(3):
            self._criar_usuario(f'u{indice}', '51999990000')

        apps = self._migrar(ATUAL)

        telefone = apps.get_model('usuarios', 'Telefone')
        self.assertEqual(telefone.objects.count(), 3)
        self.assertEqual(telefone.objects.filter(e_principal=True).count(), 3)

    def test_campo_antigo_e_removido_do_usuario(self):
        self._criar_usuario('campo', '51999990000')

        apps = self._migrar(ATUAL)

        campos = [campo.name for campo in apps.get_model('usuarios', 'Usuario')._meta.get_fields()]
        self.assertNotIn('telefone', campos)
        self.assertIn('telefones', campos)

    def test_seed_dos_tipos_e_idempotente(self):
        tipo = self.apps_antes.get_model('usuarios', 'TipoTelefone')
        tipo.objects.all().delete()

        apps = self._migrar(ATUAL)
        descricoes = list(apps.get_model('usuarios', 'TipoTelefone').objects.order_by('id').values_list('descricao', flat=True))
        self.assertEqual(descricoes, ['Celular', 'Fixo', 'Comercial'])

        self._migrar(ANTES)
        apps = self._migrar(ATUAL)
        descricoes = list(apps.get_model('usuarios', 'TipoTelefone').objects.order_by('id').values_list('descricao', flat=True))
        self.assertEqual(descricoes, ['Celular', 'Fixo', 'Comercial'])

    def test_reversao_devolve_o_telefone_principal_ao_usuario_e_descarta_os_demais(self):
        com_principal = self._criar_usuario('rev', '51999990000')
        sem_telefone = self._criar_usuario('rev-sem', None)
        apps = self._migrar(ATUAL)
        telefone = apps.get_model('usuarios', 'Telefone')
        fixo = apps.get_model('usuarios', 'TipoTelefone').objects.get(descricao='Fixo')
        telefone.objects.filter(usuario_id=com_principal).update(numero='51988887777')
        telefone.objects.create(usuario_id=com_principal, tipo=fixo, numero='5133334444', e_principal=False)

        apps_revertidas = self._migrar(ANTES)

        usuario = apps_revertidas.get_model('usuarios', 'Usuario')
        self.assertEqual(usuario.objects.get(pk=com_principal).telefone, '51988887777')
        self.assertIsNone(usuario.objects.get(pk=sem_telefone).telefone)
        self.assertEqual(apps_revertidas.get_model('usuarios', 'Telefone').objects.count(), 0)

    def _criar_usuario(self, nome, telefone):
        genero_model = self.apps_antes.get_model('usuarios', 'Genero')
        usuario_model = self.apps_antes.get_model('usuarios', 'Usuario')
        genero, _ = genero_model.objects.get_or_create(id_genero='Z', defaults={'genero': 'Teste Migração'})
        usuario = usuario_model.objects.create(
            cpf=f'{abs(hash(nome)) % 10**11:011d}', email=f'{nome}@migracao.test', nome=nome, data_nascimento='1990-01-01',
            genero=genero, password='x', foto_perfil='', telefone=telefone,
        )
        return usuario.pk

    def _telefone(self, apps, usuario_id):
        return apps.get_model('usuarios', 'Telefone').objects.select_related('tipo').get(usuario_id=usuario_id)

    def _migrar_para_folhas(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())

    def _migrar(self, alvo):
        executor = MigrationExecutor(connection)
        executor.migrate(alvo)
        executor = MigrationExecutor(connection)
        return executor.loader.project_state(alvo).apps
