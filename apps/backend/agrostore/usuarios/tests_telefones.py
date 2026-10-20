from datetime import date
from io import StringIO

from django.core.management import call_command
from django.db import IntegrityError, connection, transaction
from django.test.utils import CaptureQueriesContext
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase

from agrostore.lojas.models import Loja
from agrostore.pedidos.models import Pedido, PedidoCliente, StatusPedido
from . import telefones as servico
from .models import Genero, Telefone, TipoTelefone, Usuario

URL_TELEFONES = '/api/v1/usuarios/me/telefones/'
URL_CADASTRO = '/api/v1/usuarios/cadastro/'
URL_ME = '/api/v1/usuarios/me/'


def tipo(descricao):
    return TipoTelefone.objects.get(descricao=descricao)


def criar_telefone(usuario, numero='51999990000', descricao='Celular', e_principal=True):
    return Telefone.objects.create(usuario=usuario, tipo=tipo(descricao), numero=numero, e_principal=e_principal)


class BaseTelefoneTests(APITestCase):
    senha = 'SenhaForte123'

    def setUp(self):
        self.genero, _ = Genero.objects.get_or_create(id_genero='M', defaults={'genero': 'Masculino'})
        self.usuario = self.criar_usuario('52998224725', 'tel@example.com')
        self.outro = self.criar_usuario('11144477735', 'outro-tel@example.com')

    def criar_usuario(self, cpf, email, **campos):
        return Usuario.objects.create_user(
            cpf=cpf, email=email, password=self.senha, nome='Usuário Tel', data_nascimento=date(2000, 1, 1),
            genero=self.genero, **campos,
        )


class TiposTelefonePublicosTests(APITestCase):
    url = '/api/v1/tipos-telefone/'

    def test_lista_os_tres_tipos_sem_autenticacao(self):
        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual([item['descricao'] for item in resposta.data], ['Celular', 'Fixo', 'Comercial'])
        self.assertEqual(set(resposta.data[0]), {'id', 'descricao'})

    def test_token_invalido_nao_derruba_a_listagem_publica(self):
        resposta = self.client.get(self.url, HTTP_AUTHORIZATION='Bearer token-invalido')

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)

    def test_nao_aceita_escrita(self):
        for metodo in (self.client.post, self.client.put, self.client.patch, self.client.delete):
            self.assertEqual(metodo(self.url, {'descricao': 'Novo'}, format='json').status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(TipoTelefone.objects.count(), 3)


class CadastroComTelefoneTests(BaseTelefoneTests):
    def dados(self, **campos):
        dados = {
            'nome': 'Cliente Novo', 'cpf': '529.982.247-25', 'email': 'novo@example.com', 'telefone': '(51) 99999-0000',
            'tipo_telefone': tipo('Celular').pk, 'data_nascimento': '2000-05-10', 'genero': 'M',
            'password': self.senha, 'password_confirmacao': self.senha,
        }
        dados.update(campos)
        return dados

    def setUp(self):
        super().setUp()
        Usuario.objects.all().delete()

    def test_cadastro_valido_retorna_telefone_principal_com_tipo(self):
        resposta = self.client.post(URL_CADASTRO, self.dados(), format='json')

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        telefone = Telefone.objects.get()
        self.assertEqual(resposta.data['usuario']['telefones'], [{
            'id': telefone.pk, 'numero': '51999990000', 'tipo': tipo('Celular').pk, 'tipo_descricao': 'Celular', 'e_principal': True,
        }])

    def test_cadastro_aceita_cada_tipo_com_a_quantidade_de_digitos_correta(self):
        casos = [('Celular', '51999990000'), ('Fixo', '5133334444'), ('Comercial', '5133334444'), ('Comercial', '51999990000')]
        for indice, (descricao, numero) in enumerate(casos):
            cpf = ['52998224725', '11144477735', '39053344705', '15350946056'][indice]
            dados = self.dados(cpf=cpf, email=f'c{indice}@example.com', telefone=numero, tipo_telefone=tipo(descricao).pk)
            resposta = self.client.post(URL_CADASTRO, dados, format='json')
            self.assertEqual(resposta.status_code, status.HTTP_201_CREATED, (descricao, numero, resposta.data))

    def test_cadastro_recusa_quantidade_de_digitos_invalida_por_tipo(self):
        casos = [
            ('Celular', '5133334444', 'Celular deve ter 11 dígitos com DDD.'),
            ('Fixo', '51999990000', 'Telefone fixo deve ter 10 dígitos com DDD.'),
            ('Comercial', '513333444', 'Telefone comercial deve ter 10 ou 11 dígitos com DDD.'),
            ('Comercial', '519999900001', 'Telefone comercial deve ter 10 ou 11 dígitos com DDD.'),
        ]
        for descricao, numero, mensagem in casos:
            resposta = self.client.post(URL_CADASTRO, self.dados(telefone=numero, tipo_telefone=tipo(descricao).pk), format='json')
            self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST, (descricao, numero))
            self.assertEqual(resposta.data['telefone'], [mensagem])
        self.assertFalse(Usuario.objects.exists())

    def test_cadastro_recusa_tipo_inexistente(self):
        resposta = self.client.post(URL_CADASTRO, self.dados(tipo_telefone=9999), format='json')

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resposta.data['tipo_telefone'], ['Informe um tipo de telefone válido.'])
        self.assertFalse(Usuario.objects.exists())

    def test_cadastro_recusa_tipo_nao_numerico(self):
        resposta = self.client.post(URL_CADASTRO, self.dados(tipo_telefone='abc'), format='json')

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('tipo_telefone', resposta.data)

    def test_cadastro_exige_tipo_e_telefone(self):
        for campo in ('tipo_telefone', 'telefone'):
            dados = self.dados()
            del dados[campo]
            resposta = self.client.post(URL_CADASTRO, dados, format='json')
            self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST, campo)
            self.assertIn(campo, resposta.data)
        self.assertFalse(Usuario.objects.exists())

    def test_cadastro_com_telefone_invalido_nao_cria_usuario_nem_telefone(self):
        resposta = self.client.post(URL_CADASTRO, self.dados(telefone='123'), format='json')

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Usuario.objects.exists())
        self.assertFalse(Telefone.objects.exists())

    def test_cadastro_aceita_mesmo_numero_de_outro_usuario(self):
        criar_telefone(self.criar_usuario('39053344705', 'outro@example.com'), '51999990000')

        resposta = self.client.post(URL_CADASTRO, self.dados(), format='json')

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Telefone.objects.filter(numero='51999990000').count(), 2)


class PerfilTelefoneTests(BaseTelefoneTests):
    def test_me_lista_telefones_com_principal_primeiro(self):
        secundario = criar_telefone(self.usuario, '5133334444', 'Fixo', e_principal=False)
        principal = criar_telefone(self.usuario, '51999990000')
        self.client.force_authenticate(self.usuario)

        resposta = self.client.get(URL_ME)

        self.assertEqual([t['id'] for t in resposta.data['telefones']], [principal.pk, secundario.pk])
        self.assertNotIn('telefone', resposta.data)

    def test_me_devolve_lista_vazia_na_conta_legada(self):
        self.client.force_authenticate(self.usuario)

        resposta = self.client.get(URL_ME)

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data['telefones'], [])

    def test_patch_me_com_telefone_e_recusado_sem_alterar_nada(self):
        criar_telefone(self.usuario)
        self.client.force_authenticate(self.usuario)

        resposta = self.client.patch(URL_ME, {'telefone': '51988887777'}, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', resposta.data)
        self.assertEqual(self.usuario.telefones.get().numero, '51999990000')

    def test_patch_me_com_telefone_junto_de_campo_valido_nao_altera_o_nome(self):
        self.client.force_authenticate(self.usuario)

        resposta = self.client.patch(URL_ME, {'nome': 'Outro Nome', 'telefones': []}, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.nome, 'Usuário Tel')


class TelefoneApiTests(BaseTelefoneTests):
    def setUp(self):
        super().setUp()
        self.principal = criar_telefone(self.usuario, '51999990000')
        self.client.force_authenticate(self.usuario)

    def url(self, telefone):
        return f'{URL_TELEFONES}{telefone.pk}/'

    def test_lista_e_detalha_somente_os_proprios_telefones(self):
        criar_telefone(self.outro, '51988887777')

        lista = self.client.get(URL_TELEFONES)
        detalhe = self.client.get(self.url(self.principal))

        self.assertEqual(lista.status_code, status.HTTP_200_OK)
        self.assertEqual([t['numero'] for t in lista.data], ['51999990000'])
        self.assertEqual(detalhe.data['tipo_descricao'], 'Celular')

    def test_outro_usuario_recebe_404_em_detalhe_edicao_e_exclusao(self):
        alheio = criar_telefone(self.outro, '51988887777')

        self.assertEqual(self.client.get(self.url(alheio)).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.patch(self.url(alheio), {'numero': '51977776666'}, format='json').status_code, 404)
        self.assertEqual(self.client.patch(self.url(alheio), {'e_principal': True}, format='json').status_code, 404)
        self.assertEqual(self.client.delete(self.url(alheio)).status_code, status.HTTP_404_NOT_FOUND)
        alheio.refresh_from_db()
        self.assertEqual(alheio.numero, '51988887777')

    def test_exige_autenticacao(self):
        self.client.force_authenticate(user=None)

        self.assertEqual(self.client.get(URL_TELEFONES).status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.client.post(URL_TELEFONES, {}, format='json').status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.client.get(self.url(self.principal)).status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.client.delete(self.url(self.principal)).status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_nao_e_permitido(self):
        dados = {'numero': '51977776666', 'tipo': tipo('Celular').pk}

        self.assertEqual(self.client.put(self.url(self.principal), dados, format='json').status_code, 405)
        self.assertEqual(self.client.put(URL_TELEFONES, dados, format='json').status_code, 405)

    def test_cria_telefone_normalizando_o_numero_e_sem_virar_principal(self):
        dados = {'numero': '(51) 3333-4444', 'tipo': tipo('Fixo').pk}

        resposta = self.client.post(URL_TELEFONES, dados, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resposta.data['numero'], '5133334444')
        self.assertFalse(resposta.data['e_principal'])
        self.assertEqual(Telefone.objects.get(pk=self.principal.pk).e_principal, True)

    def test_cria_telefone_ja_como_principal_desmarca_o_anterior(self):
        dados = {'numero': '51988887777', 'tipo': tipo('Celular').pk, 'e_principal': True}

        resposta = self.client.post(URL_TELEFONES, dados, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertTrue(resposta.data['e_principal'])
        self.principal.refresh_from_db()
        self.assertFalse(self.principal.e_principal)
        self.assertEqual(self.usuario.telefones.filter(e_principal=True).count(), 1)

    def test_nao_ha_limite_de_quantidade_de_telefones(self):
        for indice in range(6):
            resposta = self.client.post(URL_TELEFONES, {'numero': f'5199999000{indice}', 'tipo': tipo('Celular').pk}, format='json')
            self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.usuario.telefones.count(), 7)

    def test_dono_vem_do_token_e_nao_do_corpo(self):
        dados = {'numero': '51988887777', 'tipo': tipo('Celular').pk, 'usuario': self.outro.pk}

        self.client.post(URL_TELEFONES, dados, format='json')

        self.assertFalse(self.outro.telefones.exists())
        self.assertEqual(self.usuario.telefones.count(), 2)

    def test_criacao_valida_digitos_pelo_tipo_e_tipo_inexistente(self):
        casos = [
            ({'numero': '5133334444', 'tipo': tipo('Celular').pk}, 'numero', 'Celular deve ter 11 dígitos com DDD.'),
            ({'numero': '51999990000', 'tipo': tipo('Fixo').pk}, 'numero', 'Telefone fixo deve ter 10 dígitos com DDD.'),
            ({'numero': '51999990000', 'tipo': 9999}, 'tipo', 'Informe um tipo de telefone válido.'),
        ]
        for dados, campo, mensagem in casos:
            resposta = self.client.post(URL_TELEFONES, dados, format='json')
            self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST, dados)
            self.assertEqual(resposta.data[campo], [mensagem])
        self.assertEqual(self.usuario.telefones.count(), 1)

    def test_criacao_exige_numero_e_tipo(self):
        resposta = self.client.post(URL_TELEFONES, {}, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('numero', resposta.data)
        self.assertIn('tipo', resposta.data)

    def test_edita_o_numero_mantendo_o_tipo(self):
        resposta = self.client.patch(self.url(self.principal), {'numero': '(51) 97777-6666'}, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.principal.refresh_from_db()
        self.assertEqual(self.principal.numero, '51977776666')
        self.assertTrue(self.principal.e_principal)

    def test_legado_fora_do_padrao_vira_principal_pela_api_sem_revalidar_o_numero(self):
        legado = criar_telefone(self.usuario, '519999000', 'Celular', e_principal=False)

        resposta = self.client.patch(self.url(legado), {'e_principal': True}, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        legado.refresh_from_db()
        self.principal.refresh_from_db()
        self.assertEqual((legado.e_principal, legado.numero), (True, '519999000'))
        self.assertFalse(self.principal.e_principal)

    def test_legado_fora_do_padrao_continua_exigindo_numero_valido_ao_editar_o_numero(self):
        legado = criar_telefone(self.usuario, '519999000', 'Celular', e_principal=False)

        resposta = self.client.patch(self.url(legado), {'numero': '5199999000'}, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_me_nao_tem_n_mais_um_ao_aumentar_os_telefones(self):
        self.client.force_authenticate(Usuario.objects.get(pk=self.usuario.pk))
        with CaptureQueriesContext(connection) as com_um_telefone:
            self.client.get(URL_ME)
        criar_telefone(self.usuario, '5133334444', 'Fixo', e_principal=False)
        criar_telefone(self.usuario, '5133335555', 'Comercial', e_principal=False)

        self.client.force_authenticate(Usuario.objects.get(pk=self.usuario.pk))
        with self.assertNumQueries(len(com_um_telefone)):
            resposta = self.client.get(URL_ME)
        self.assertEqual(len(resposta.data['telefones']), 3)

    def test_trocar_o_tipo_revalida_o_numero_existente(self):
        resposta = self.client.patch(self.url(self.principal), {'tipo': tipo('Fixo').pk}, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resposta.data['numero'], ['Telefone fixo deve ter 10 dígitos com DDD.'])
        self.principal.refresh_from_db()
        self.assertEqual(self.principal.tipo.descricao, 'Celular')

    def test_trocar_para_comercial_aceita_celular_de_11_digitos(self):
        resposta = self.client.patch(self.url(self.principal), {'tipo': tipo('Comercial').pk}, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data['tipo_descricao'], 'Comercial')

    def test_trocar_tipo_e_numero_juntos(self):
        dados = {'tipo': tipo('Fixo').pk, 'numero': '5133334444'}

        resposta = self.client.patch(self.url(self.principal), dados, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual((resposta.data['tipo_descricao'], resposta.data['numero']), ('Fixo', '5133334444'))

    def test_definir_outro_principal_desmarca_o_anterior(self):
        segundo = criar_telefone(self.usuario, '5133334444', 'Fixo', e_principal=False)

        resposta = self.client.patch(self.url(segundo), {'e_principal': True}, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.principal.refresh_from_db()
        segundo.refresh_from_db()
        self.assertFalse(self.principal.e_principal)
        self.assertTrue(segundo.e_principal)
        self.assertEqual(self.client.get(URL_TELEFONES).data[0]['id'], segundo.pk)

    def test_nao_e_possivel_desmarcar_o_principal_sem_definir_outro(self):
        resposta = self.client.patch(self.url(self.principal), {'e_principal': False}, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resposta.data['e_principal'], ['Defina outro telefone como principal.'])
        self.principal.refresh_from_db()
        self.assertTrue(self.principal.e_principal)

    def test_exclui_telefone_nao_principal(self):
        segundo = criar_telefone(self.usuario, '5133334444', 'Fixo', e_principal=False)

        resposta = self.client.delete(self.url(segundo))

        self.assertEqual(resposta.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Telefone.objects.filter(pk=segundo.pk).exists())

    def test_exclusao_do_ultimo_telefone_e_bloqueada(self):
        resposta = self.client.delete(self.url(self.principal))

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resposta.data['detail'], 'Você precisa manter ao menos um telefone.')
        self.assertTrue(Telefone.objects.filter(pk=self.principal.pk).exists())

    def test_exclusao_do_principal_com_outros_telefones_e_bloqueada(self):
        criar_telefone(self.usuario, '5133334444', 'Fixo', e_principal=False)

        resposta = self.client.delete(self.url(self.principal))

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resposta.data['detail'], 'Defina outro telefone como principal antes de excluir este.')
        self.assertEqual(self.usuario.telefones.count(), 2)

    def test_exclui_o_antigo_principal_depois_de_definir_outro(self):
        segundo = criar_telefone(self.usuario, '5133334444', 'Fixo', e_principal=False)
        self.client.patch(self.url(segundo), {'e_principal': True}, format='json')

        resposta = self.client.delete(self.url(self.principal))

        self.assertEqual(resposta.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.usuario.telefones.get().pk, segundo.pk)

    def test_exclusao_do_telefone_de_um_usuario_nao_afeta_o_outro(self):
        criar_telefone(self.outro, '51988887777')
        resposta = self.client.delete(self.url(self.principal))

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.outro.telefones.count(), 1)


class ContaLegadaSemTelefoneTests(BaseTelefoneTests):
    """Exceção legada: conta com 0 telefones continua funcionando."""

    def test_login_funciona_sem_telefone(self):
        resposta = self.client.post('/api/v1/usuarios/login/', {'cpf': '52998224725', 'password': self.senha}, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data['usuario']['telefones'], [])

    def test_primeiro_telefone_vira_principal_automaticamente_pela_api(self):
        self.client.force_authenticate(self.usuario)

        resposta = self.client.post(URL_TELEFONES, {'numero': '5133334444', 'tipo': tipo('Fixo').pk}, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertTrue(resposta.data['e_principal'])

    def test_primeiro_telefone_vira_principal_mesmo_com_e_principal_falso(self):
        self.client.force_authenticate(self.usuario)

        resposta = self.client.post(
            URL_TELEFONES, {'numero': '5133334444', 'tipo': tipo('Fixo').pk, 'e_principal': False}, format='json',
        )

        self.assertTrue(resposta.data['e_principal'])

    def test_segundo_telefone_nao_vira_principal(self):
        self.client.force_authenticate(self.usuario)
        self.client.post(URL_TELEFONES, {'numero': '5133334444', 'tipo': tipo('Fixo').pk}, format='json')

        resposta = self.client.post(URL_TELEFONES, {'numero': '51999990000', 'tipo': tipo('Celular').pk}, format='json')

        self.assertFalse(resposta.data['e_principal'])

    def test_lista_vazia_e_nao_ha_o_que_excluir(self):
        self.client.force_authenticate(self.usuario)

        self.assertEqual(self.client.get(URL_TELEFONES).data, [])


class PrincipalUnicoNoBancoTests(BaseTelefoneTests):
    def test_banco_recusa_dois_principais_do_mesmo_usuario(self):
        criar_telefone(self.usuario, '51999990000')

        with self.assertRaises(IntegrityError), transaction.atomic():
            criar_telefone(self.usuario, '51988887777', e_principal=True)

        self.assertEqual(self.usuario.telefones.count(), 1)

    def test_banco_aceita_um_principal_por_usuario_e_varios_nao_principais(self):
        criar_telefone(self.usuario, '51999990000')
        criar_telefone(self.outro, '51999990000')
        criar_telefone(self.usuario, '5133334444', 'Fixo', e_principal=False)
        criar_telefone(self.usuario, '5133335555', 'Fixo', e_principal=False)

        self.assertEqual(Telefone.objects.filter(e_principal=True).count(), 2)

    def test_tipo_com_telefone_nao_pode_ser_excluido(self):
        from django.db.models import ProtectedError
        criar_telefone(self.usuario)

        with self.assertRaises(ProtectedError):
            tipo('Celular').delete()

    def test_excluir_usuario_remove_seus_telefones(self):
        criar_telefone(self.usuario)
        criar_telefone(self.outro, '51988887777')

        self.usuario.delete()

        self.assertEqual(Telefone.objects.count(), 1)


class ServicoTelefoneTests(BaseTelefoneTests):
    def test_validar_numero_remove_formatacao(self):
        self.assertEqual(servico.validar_numero_por_tipo('(51) 99999-0000', tipo('Celular')), '51999990000')

    def test_validar_numero_recusa_quantidade_errada(self):
        with self.assertRaises(servico.RegraTelefoneViolada):
            servico.validar_numero_por_tipo('519999900', tipo('Celular'))

    def test_criar_telefone_do_servico_torna_o_primeiro_principal(self):
        telefone = servico.criar_telefone(self.usuario, '51999990000', tipo('Celular'))

        self.assertTrue(telefone.e_principal)

    def test_atualizar_telefone_legado_fora_do_padrao_pode_virar_principal_sem_revalidar(self):
        criar_telefone(self.usuario, '51999990000')
        legado = criar_telefone(self.usuario, '123456', 'Celular', e_principal=False)

        servico.atualizar_telefone(legado, e_principal=True)

        legado.refresh_from_db()
        self.assertTrue(legado.e_principal)
        self.assertEqual(self.usuario.telefones.filter(e_principal=True).count(), 1)


class ComandoTelefonesForaDoPadraoTests(BaseTelefoneTests):
    def executar(self):
        saida = StringIO()
        call_command('telefones_fora_do_padrao', stdout=saida)
        return saida.getvalue()

    def test_informa_quando_nao_ha_telefone_fora_do_padrao(self):
        criar_telefone(self.usuario)

        self.assertIn('Nenhum telefone fora do padrão.', self.executar())

    def test_informa_quando_nao_ha_telefones(self):
        self.assertIn('Nenhum telefone fora do padrão.', self.executar())

    def test_lista_ids_tipo_e_digitos_sem_expor_o_numero(self):
        correto = criar_telefone(self.usuario, '51999990000')
        errado = criar_telefone(self.outro, '1234567', 'Celular')

        saida = self.executar()

        self.assertIn(f'usuario={self.outro.pk} telefone={errado.pk} tipo=Celular digitos=7', saida)
        self.assertNotIn('1234567', saida.replace('digitos=7', ''))
        self.assertNotIn(f'telefone={correto.pk} ', saida)
        self.assertNotIn('51999990000', saida)

    def test_e_somente_leitura(self):
        errado = criar_telefone(self.usuario, '1234567')

        self.executar()

        errado.refresh_from_db()
        self.assertEqual((errado.numero, errado.e_principal), ('1234567', True))
        self.assertEqual(Telefone.objects.count(), 1)


class AdminTelefoneTests(BaseTelefoneTests):
    def setUp(self):
        super().setUp()
        self.admin = self.criar_usuario('39053344705', 'admin-tel@example.com', is_staff=True, is_superuser=True)
        self.principal = criar_telefone(self.usuario, '51999990000')
        self.client.force_login(self.admin)
        self.url = f'/admin/usuarios/usuario/{self.usuario.pk}/change/'

    def dados(self, formularios, iniciais=None):
        dados = {
            'nome': self.usuario.nome, 'cpf': self.usuario.cpf, 'email': self.usuario.email,
            'data_nascimento': '2000-01-01', 'genero': 'M', 'is_active': 'on',
            'telefones-TOTAL_FORMS': str(len(formularios)),
            'telefones-INITIAL_FORMS': str(self.usuario.telefones.count() if iniciais is None else iniciais),
            'telefones-MIN_NUM_FORMS': '1', 'telefones-MAX_NUM_FORMS': '1000',
        }
        for indice, formulario in enumerate(formularios):
            for campo, valor in formulario.items():
                if valor is not None and valor is not False:
                    dados[f'telefones-{indice}-{campo}'] = 'on' if valor is True else str(valor)
            dados[f'telefones-{indice}-usuario'] = str(self.usuario.pk)
        return dados

    def form_existente(self, telefone, **campos):
        base = {'id': telefone.pk, 'tipo': telefone.tipo_id, 'numero': telefone.numero, 'principal': telefone.e_principal}
        base.update(campos)
        return base

    def novo(self, numero, descricao, principal=False):
        return {'tipo': tipo(descricao).pk, 'numero': numero, 'principal': principal}

    def salvar(self, formularios, iniciais=None):
        return self.client.post(self.url, self.dados(formularios, iniciais))

    def test_pagina_do_usuario_exibe_o_inline_de_telefones(self):
        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'telefones-TOTAL_FORMS')

    def test_adiciona_telefone_mantendo_o_principal(self):
        resposta = self.salvar([self.form_existente(self.principal), self.novo('5133334444', 'Fixo')], iniciais=1)

        self.assertEqual(resposta.status_code, 302, getattr(resposta, 'context_data', None) and resposta.context_data['errors'])
        self.assertEqual(self.usuario.telefones.count(), 2)
        self.assertEqual(self.usuario.telefones.filter(e_principal=True).get().pk, self.principal.pk)

    def test_troca_o_principal_sem_violar_a_constraint(self):
        segundo = criar_telefone(self.usuario, '5133334444', 'Fixo', e_principal=False)

        resposta = self.salvar([self.form_existente(self.principal, principal=False), self.form_existente(segundo, principal=True)])

        self.assertEqual(resposta.status_code, 302)
        self.principal.refresh_from_db()
        segundo.refresh_from_db()
        self.assertEqual((self.principal.e_principal, segundo.e_principal), (False, True))

    def test_novo_telefone_pode_ser_o_principal(self):
        resposta = self.salvar([self.form_existente(self.principal, principal=False), self.novo('51988887777', 'Celular', True)], 1)

        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(self.usuario.telefones.filter(e_principal=True).get().numero, '51988887777')
        self.assertEqual(self.usuario.telefones.count(), 2)

    def test_recusa_dois_principais(self):
        segundo = criar_telefone(self.usuario, '5133334444', 'Fixo', e_principal=False)

        resposta = self.salvar([self.form_existente(self.principal, principal=True), self.form_existente(segundo, principal=True)])

        self.assertEqual(resposta.status_code, 200)
        segundo.refresh_from_db()
        self.assertFalse(segundo.e_principal)
        self.assertContains(resposta, 'Marque exatamente um telefone como principal.')

    def test_recusa_nenhum_principal(self):
        resposta = self.salvar([self.form_existente(self.principal, principal=False)])

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Marque exatamente um telefone como principal.')
        self.principal.refresh_from_db()
        self.assertTrue(self.principal.e_principal)

    def test_recusa_excluir_o_unico_telefone(self):
        resposta = self.salvar([self.form_existente(self.principal, DELETE=True)])

        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(Telefone.objects.filter(pk=self.principal.pk).exists())

    def test_recusa_excluir_o_principal_sem_marcar_outro(self):
        segundo = criar_telefone(self.usuario, '5133334444', 'Fixo', e_principal=False)

        resposta = self.salvar([self.form_existente(self.principal, DELETE=True), self.form_existente(segundo)])

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(self.usuario.telefones.count(), 2)

    def test_exclui_o_principal_ao_marcar_outro(self):
        segundo = criar_telefone(self.usuario, '5133334444', 'Fixo', e_principal=False)

        resposta = self.salvar([self.form_existente(self.principal, DELETE=True), self.form_existente(segundo, principal=True)])

        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(self.usuario.telefones.get().pk, segundo.pk)
        segundo.refresh_from_db()
        self.assertTrue(segundo.e_principal)

    def test_valida_digitos_pelo_tipo(self):
        resposta = self.salvar([self.form_existente(self.principal), self.novo('51999990000', 'Fixo')], iniciais=1)

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Telefone fixo deve ter 10 dígitos com DDD.')
        self.assertEqual(self.usuario.telefones.count(), 1)

    def test_editar_o_tipo_revalida_o_numero(self):
        resposta = self.salvar([self.form_existente(self.principal, tipo=tipo('Fixo').pk)])

        self.assertEqual(resposta.status_code, 200)
        self.principal.refresh_from_db()
        self.assertEqual(self.principal.tipo.descricao, 'Celular')

    def test_conta_legada_sem_telefone_nao_salva_sem_informar_um(self):
        legado = self.criar_usuario('15350946056', 'legado@example.com')
        dados = self.dados([])
        dados.update({'cpf': legado.cpf, 'email': legado.email, 'telefones-INITIAL_FORMS': '0'})

        resposta = self.client.post(f'/admin/usuarios/usuario/{legado.pk}/change/', dados)

        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(legado.telefones.exists())

    def test_conta_legada_salva_ao_informar_um_telefone_principal(self):
        legado = self.criar_usuario('15350946056', 'legado@example.com')
        dados = self.dados([self.novo('51999990000', 'Celular', True)])
        dados.update({'cpf': legado.cpf, 'email': legado.email, 'telefones-INITIAL_FORMS': '0'})
        dados['telefones-0-usuario'] = str(legado.pk)

        resposta = self.client.post(f'/admin/usuarios/usuario/{legado.pk}/change/', dados)

        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(legado.telefones.get().e_principal)

    def test_pagina_de_adicao_exige_telefone(self):
        dados = {
            'nome': 'Novo Admin', 'cpf': '86288366757', 'email': 'novo-admin@example.com', 'data_nascimento': '2000-01-01',
            'genero': 'M', 'is_active': 'on', 'password1': self.senha, 'password2': self.senha,
            'telefones-TOTAL_FORMS': '0', 'telefones-INITIAL_FORMS': '0', 'telefones-MIN_NUM_FORMS': '1',
            'telefones-MAX_NUM_FORMS': '1000',
        }

        resposta = self.client.post('/admin/usuarios/usuario/add/', dados)

        self.assertIn(resposta.status_code, (200, 400))
        self.assertFalse(Usuario.objects.filter(email='novo-admin@example.com').exists())


class PedidoNaoDependeDoTelefoneTests(BaseTelefoneTests):
    def test_excluir_telefone_nao_afeta_pedidos_do_cliente(self):
        produtor = self.criar_usuario('86288366757', 'prod-tel@example.com', is_produtor=True)
        loja = Loja.objects.create(proprietario=produtor, nome='Loja', cnpj='11222333000181')
        pedido = Pedido.objects.create(loja=loja, status=StatusPedido.objects.create(status='Pendente'))
        PedidoCliente.objects.create(
            pedido=pedido, usuario=self.usuario, nome='X', cpf=self.usuario.cpf, email=self.usuario.email,
            data_nascimento=self.usuario.data_nascimento, genero='Masculino',
        )
        criar_telefone(self.usuario)
        criar_telefone(self.usuario, '5133334444', 'Fixo', e_principal=False)

        self.usuario.telefones.filter(e_principal=False).delete()

        self.assertTrue(PedidoCliente.objects.filter(pedido=pedido).exists())


class SeedTiposTelefoneTests(TestCase):
    def test_tipos_fixos_existem_sem_duplicidade(self):
        self.assertEqual(list(TipoTelefone.objects.values_list('descricao', flat=True)), ['Celular', 'Fixo', 'Comercial'])
