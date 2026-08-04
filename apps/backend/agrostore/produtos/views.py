from rest_framework import permissions, serializers, viewsets
from rest_framework.exceptions import PermissionDenied
from .models import Produto, PrecoProduto, Categoria
from .serializers import ProdutoSerializer, PrecoProdutoSerializer, CategoriaSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_queryset(self):
        queryset = super().get_queryset()
        ativo = self.request.query_params.get('ativo')

        if ativo is None:
            return queryset
        if ativo.lower() == 'true':
            return queryset.filter(ativo=True)
        if ativo.lower() == 'false':
            return queryset.filter(ativo=False)
        raise serializers.ValidationError({'ativo': 'Informe true ou false.'})

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        if self.action == 'partial_update':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        usuario = self.request.user
        if not usuario.is_produtor and not usuario.is_staff:
            raise PermissionDenied('Somente produtores podem sugerir categorias.')

        if usuario.is_staff:
            serializer.save()
            return

        serializer.save(ativo=False)

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

    def get_queryset(self):
        queryset = super().get_queryset()
        categoria_id = self.request.query_params.get('categoria')

        if categoria_id is None:
            return queryset
        if not categoria_id.isdigit():
            raise serializers.ValidationError({'categoria': 'Informe o identificador numérico da categoria.'})
        return queryset.filter(categoria_id=categoria_id)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
