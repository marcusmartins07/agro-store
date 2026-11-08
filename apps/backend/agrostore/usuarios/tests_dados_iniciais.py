import importlib

from django.apps import apps
from django.test import TestCase

from .models import Genero, TipoTelefone

dados_iniciais = importlib.import_module('agrostore.usuarios.migrations.0002_dados_iniciais')


def executar_seed():
    dados_iniciais.criar_dados_iniciais(apps, None)


class DadosIniciaisTests(TestCase):
    def test_banco_migrado_possui_generos_e_tipos_de_telefone_padrao(self):
        generos = dict(Genero.objects.values_list('id_genero', 'genero'))
        self.assertEqual(generos['M'], 'Masculino')
        self.assertEqual(generos['F'], 'Feminino')
        self.assertEqual(generos['I'], 'Prefiro não informar')
        descricoes = set(TipoTelefone.objects.values_list('descricao', flat=True))
        self.assertTrue({'Celular', 'Fixo', 'Comercial'} <= descricoes)

    def test_seed_executado_duas_vezes_nao_duplica_registros(self):
        executar_seed()
        executar_seed()
        self.assertEqual(Genero.objects.count(), 3)
        self.assertEqual(TipoTelefone.objects.count(), 3)

    def test_seed_renomeia_indefinido_para_prefiro_nao_informar(self):
        Genero.objects.filter(id_genero='I').update(genero='Indefinido')
        executar_seed()
        self.assertEqual(Genero.objects.get(id_genero='I').genero, 'Prefiro não informar')

    def test_seed_nao_sobrescreve_genero_renomeado_pelo_admin(self):
        Genero.objects.filter(id_genero='M').update(genero='Homem')
        Genero.objects.filter(id_genero='I').update(genero='Não declarado')
        executar_seed()
        self.assertEqual(Genero.objects.get(id_genero='M').genero, 'Homem')
        self.assertEqual(Genero.objects.get(id_genero='I').genero, 'Não declarado')
