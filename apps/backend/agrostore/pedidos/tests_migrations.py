from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase

ANTES = [('pedidos', '0002_pedidocliente_telefone')]
ETAPA_SCHEMA = [('pedidos', '0003_pedidocliente_usuario')]
ATUAL = [('pedidos', '0006_remove_pedidocliente_telefone')]


class MigracaoVinculoClienteTests(TransactionTestCase):
    """O usuário do pedido passa de Pedido.usuario para PedidoCliente.usuario."""

    def setUp(self):
        self.apps_antes = self._migrar(ANTES)

    def tearDown(self):
        self._migrar(ETAPA_SCHEMA)
        self._apagar_dados()
        self._migrar_para_folhas()

    def test_migration_preserva_o_cliente_dos_pedidos_existentes(self):
        dados = self._criar_pedidos_historicos(com_snapshot=True)

        apps_depois = self._migrar(ATUAL)

        pedido_cliente = apps_depois.get_model('pedidos', 'PedidoCliente')
        for pedido_id, usuario_id in dados.items():
            self.assertEqual(pedido_cliente.objects.get(pedido_id=pedido_id).usuario_id, usuario_id)
        pedido = apps_depois.get_model('pedidos', 'Pedido')
        self.assertNotIn('usuario', [campo.name for campo in pedido._meta.get_fields()])

    def test_reversao_devolve_o_usuario_original_aos_pedidos(self):
        dados = self._criar_pedidos_historicos(com_snapshot=True)
        self._migrar(ATUAL)

        apps_revertidas = self._migrar(ANTES)

        pedido = apps_revertidas.get_model('pedidos', 'Pedido')
        self.assertEqual(pedido.objects.count(), len(dados))
        for pedido_id, usuario_id in dados.items():
            self.assertEqual(pedido.objects.get(pedido_id=pedido_id).usuario_id, usuario_id)

    def test_migration_e_interrompida_quando_ha_pedido_sem_pedido_cliente(self):
        self._criar_pedidos_historicos(com_snapshot=False)

        with self.assertRaises(RuntimeError) as contexto:
            self._migrar(ATUAL)

        self.assertIn('pedidos sem pedido_cliente', str(contexto.exception))

    def _criar_pedidos_historicos(self, com_snapshot):
        usuario_model = self.apps_antes.get_model('usuarios', 'Usuario')
        genero_model = self.apps_antes.get_model('usuarios', 'Genero')
        loja_model = self.apps_antes.get_model('lojas', 'Loja')
        pedido_model = self.apps_antes.get_model('pedidos', 'Pedido')
        pedido_cliente_model = self.apps_antes.get_model('pedidos', 'PedidoCliente')
        status_model = self.apps_antes.get_model('pedidos', 'StatusPedido')

        genero = genero_model.objects.create(id_genero='X', genero='Teste')
        status = status_model.objects.create(status='Pendente')
        usuarios = [
            usuario_model.objects.create(
                cpf=f'4234567890{i}', email=f'migracao{i}@example.com', nome=f'Cliente {i}',
                data_nascimento='1990-01-01', genero=genero, password='x', foto_perfil='',
            )
            for i in range(2)
        ]
        produtor = usuario_model.objects.create(
            cpf='42345678909', email='migracao-produtor@example.com', nome='Produtor',
            data_nascimento='1980-01-01', genero=genero, password='x', foto_perfil='',
        )
        loja = loja_model.objects.create(proprietario=produtor, nome='Loja Migração', cnpj='42345678000199')

        dados = {}
        for usuario in (usuarios[0], usuarios[0], usuarios[1]):
            pedido = pedido_model.objects.create(usuario=usuario, loja=loja, status=status)
            if com_snapshot:
                pedido_cliente_model.objects.create(
                    pedido=pedido, nome=usuario.nome, cpf=usuario.cpf, email=usuario.email,
                    data_nascimento='1990-01-01', genero='Teste',
                )
            dados[pedido.pedido_id] = usuario.pk
        return dados

    def _apagar_dados(self):
        apps = self._estado(ETAPA_SCHEMA)
        apps.get_model('pedidos', 'PedidoCliente').objects.all().delete()
        apps.get_model('pedidos', 'Pedido').objects.all().delete()
        apps.get_model('pedidos', 'StatusPedido').objects.all().delete()
        apps.get_model('lojas', 'Loja').objects.all().delete()
        apps.get_model('usuarios', 'Usuario').objects.all().delete()
        apps.get_model('usuarios', 'Genero').objects.all().delete()

    def _com_demais_apps_atualizados(self, alvo):
        folhas = MigrationExecutor(connection).loader.graph.leaf_nodes()
        return [no for no in folhas if no[0] != 'pedidos'] + alvo

    def _estado(self, alvo):
        return MigrationExecutor(connection).loader.project_state(self._com_demais_apps_atualizados(alvo)).apps

    def _migrar_para_folhas(self):
        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())

    def _migrar(self, alvo):
        MigrationExecutor(connection).migrate(self._com_demais_apps_atualizados(alvo))
        return self._estado(alvo)
