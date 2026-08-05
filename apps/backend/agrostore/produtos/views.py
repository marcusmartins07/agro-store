from rest_framework import permissions, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
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
    serializer_class = PrecoProdutoSerializer
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        queryset = PrecoProduto.objects.select_related('produto', 'produto__loja')
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(produto__loja__proprietario=self.request.user)

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        produto = serializer.validated_data['produto']
        if not self.request.user.is_staff and produto.loja.proprietario_id != self.request.user.id:
            raise PermissionDenied('Você não pode alterar o preço de um produto de outra loja.')
        serializer.save()


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.select_related('categoria', 'loja').prefetch_related('precos').all()
    serializer_class = ProdutoSerializer
    http_method_names = ['get', 'post', 'patch']

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'meus':
            if not self.request.user.is_authenticated:
                return queryset.none()
            if self.request.user.is_staff:
                return self._filtrar_categoria(queryset)
            return self._filtrar_categoria(queryset.filter(loja__proprietario=self.request.user))

        if self.action in ['update', 'partial_update']:
            if self.request.user.is_staff:
                return queryset
            return queryset.filter(loja__proprietario=self.request.user)

        queryset = queryset.filter(ativo=True, loja__ativa=True)
        return self._filtrar_categoria(queryset)

    def _filtrar_categoria(self, queryset):
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

    def perform_create(self, serializer):
        usuario = self.request.user
        if not usuario.is_produtor and not usuario.is_staff:
            raise PermissionDenied('Somente produtores podem cadastrar produtos.')

        loja = usuario.lojas.first()
        if not loja:
            raise PermissionDenied('Cadastre uma loja antes de cadastrar produtos.')
        serializer.save(loja=loja)

    @action(detail=False, methods=['get'], url_path='meus')
    def meus(self, request):
        if not request.user.is_produtor and not request.user.is_staff:
            raise PermissionDenied('Somente produtores podem consultar seus produtos.')
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
