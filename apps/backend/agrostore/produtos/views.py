from rest_framework import viewsets, permissions
from .models import Produto, PrecoProduto, Categoria
from .serializers import ProdutoSerializer, PrecoProdutoSerializer, CategoriaSerializer
from agrostore.main import bd_backup


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # bd_backup.insert_bd() #TODO somente para inserir testes
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class PrecoProdutoViewSet(viewsets.ModelViewSet):
    queryset = PrecoProduto.objects.all()
    serializer_class = PrecoProdutoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.select_related('categoria', 'loja').prefetch_related('precos').all()
    serializer_class = ProdutoSerializer
    http_method_names = ['get', 'post', 'patch']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]