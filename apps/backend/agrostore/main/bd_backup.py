from agrostore.usuarios.models import Usuario, Genero
from agrostore.produtos.models  import Categoria, Produto, PrecoProduto
from django.contrib.auth.hashers import make_password
from datetime import date
from decimal import Decimal

def insert_generos():
    generos = [
        {'id_genero': 'M', 'genero': 'Masculino'},
        {'id_genero': 'F', 'genero': 'Feminino'},
        {'id_genero': 'I', 'genero': 'Indefinido'}
    ]

    for genero in generos:
        Genero.objects.get_or_create(
            id_genero=genero['id_genero'],
            defaults={'genero': genero['genero']}
        )
        
def insert_usuarios():
    usuarios = [
        {
            "nome": "Marcus Martins",
            "cpf": "12345678900",
            "email": "marcus@email.com",
            "data_nascimento": date(2000, 5, 10),
            "genero": "M",
            "password": "123456",
            "is_produtor": False
        },
        {
            "nome": "Vinicius Silva",
            "cpf": "12345678901",
            "email": "vinicius@email.com",
            "data_nascimento": date(2000, 5, 7),
            "genero": "M",
            "password": "123456",
            "is_produtor": True
        }
    ]

    for usuario in usuarios:

        genero = Genero.objects.get(id_genero=usuario['genero'])

        if not Usuario.objects.filter(cpf=usuario['cpf']).exists():

            Usuario.objects.create_user(
                cpf=usuario['cpf'],
                nome=usuario['nome'],
                email=usuario['email'],
                data_nascimento=usuario['data_nascimento'],
                genero=genero,
                password=usuario['password'],
                is_produtor=usuario['is_produtor']
            )
            
def insert_categorias_produto():
    categorias = [
        {'categoria_id': 1, 'nome': 'Frutas'},
        {'categoria_id': 2, 'nome': 'Vegetais'},
        {'categoria_id': 3, 'nome': 'Pães'}
    ]

    for categoria in categorias:
        Categoria.objects.get_or_create(
            categoria_id=categoria['categoria_id'],
            defaults={'nome': categoria['nome']}
        )
        
def insert_produtos():
    produtos = [
        {
            "nome": "Maçã",
            "sku": "000100000001",
            "estoque": 50,
            "categoria": 1
        },
        {
            "nome": "Cenoura",
            "sku": "000200000002",
            "estoque": 50,
            "categoria": 2
        },
        {
            "nome": "Pão Francês",
            "sku": "000300000003",
            "estoque": 50,
            "categoria": 3
        }
    ]

    for produto in produtos:

        categoria = Categoria.objects.get(
            categoria_id=produto['categoria']
        )

        Produto.objects.get_or_create(
            sku=produto['sku'],
            defaults={
                "nome": produto['nome'],
                "estoque": produto['estoque'],
                "categoria": categoria,
            }
        )
        
def insert_preco():
    precos = [
        {
            "produto": 1,
            "preco_venda": "8.50",
            "preco_custo": "4.00",
            "porcentagem_desconto": 10
        },
        {
            "produto": 2,
            "preco_venda": "10",
            "preco_custo": "8",
            "porcentagem_desconto": 0
        },
        {
            "produto": 3,
            "preco_venda": "55",
            "preco_custo": "38.5",
            "porcentagem_desconto": 15
        }
    ]

    for preco in precos:

        produto = Produto.objects.get(produto_id=preco["produto"])

        PrecoProduto.objects.get_or_create(
            produto=produto,
            defaults={
                "produto": produto,
                "preco_venda": Decimal(preco["preco_venda"]),
                "preco_custo": Decimal(preco["preco_custo"]),
                "porcentagem_desconto": preco["porcentagem_desconto"],
            }
        )
        
def insert_bd():
    insert_generos()
    print('✔ Generos inseridos')

"""    insert_usuarios()
    print('✔ Usuarios inseridos')

    insert_categorias_produto()
    print('✔ Categorias inseridas')

    insert_produtos()
    print('✔ Produtos inseridos')
    
    insert_preco()
    print('✔ Preços inseridos')"""