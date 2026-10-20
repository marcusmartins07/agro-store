from django.db import transaction
from django.db.models import Max, Q
from django.shortcuts import get_object_or_404
from rest_framework import permissions, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from agrostore.carrinhos.services import ajustar_carrinhos_ao_estoque
from .models import Produto, PrecoProduto, Categoria, ImagemProduto
from .serializers import ProdutoSerializer, PrecoProdutoSerializer, CategoriaSerializer, ImagemProdutoSerializer


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
    queryset = Produto.objects.select_related('categoria', 'loja').prefetch_related('precos', 'imagens').all()
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
        if self.action == 'list':
            queryset = queryset.filter(estoque__gt=0)
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

    def perform_update(self, serializer):
        with transaction.atomic():
            Produto.objects.select_for_update().get(pk=serializer.instance.pk)
            estoque_alterado = 'estoque' in serializer.validated_data
            if not estoque_alterado:
                serializer.instance.refresh_from_db(fields=['estoque'])
            produto = serializer.save()
            if estoque_alterado:
                ajustar_carrinhos_ao_estoque(produto)

    @action(detail=False, methods=['get'], url_path='meus')
    def meus(self, request):
        if not request.user.is_produtor and not request.user.is_staff:
            raise PermissionDenied('Somente produtores podem consultar seus produtos.')
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class ImagemProdutoViewSet(viewsets.ModelViewSet):
    serializer_class = ImagemProdutoSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_produto(self):
        if not hasattr(self, '_produto'):
            produtos = Produto.objects.select_related('loja')
            usuario = self.request.user

            if not usuario.is_staff:
                if self.action in ['list', 'retrieve']:
                    visiveis = Q(ativo=True, loja__ativa=True)
                    if usuario.is_authenticated:
                        visiveis |= Q(loja__proprietario=usuario)
                    produtos = produtos.filter(visiveis)
                else:
                    produtos = produtos.filter(loja__proprietario=usuario)

            self._produto = get_object_or_404(produtos, pk=self.kwargs['produto_pk'])
        return self._produto

    def get_queryset(self):
        return ImagemProduto.objects.filter(produto=self.get_produto())

    def perform_create(self, serializer):
        produto = self.get_produto()
        tornar_principal = serializer.validated_data.pop('e_principal', False)

        with transaction.atomic():
            Produto.objects.select_for_update().get(pk=produto.pk)
            imagens = ImagemProduto.objects.filter(produto=produto)
            if imagens.count() >= ImagemProduto.LIMITE_POR_PRODUTO:
                raise serializers.ValidationError(
                    {'imagem': f'Cada produto pode ter no máximo {ImagemProduto.LIMITE_POR_PRODUTO} imagens.'}
                )

            ultima_ordem = imagens.aggregate(Max('ordem'))['ordem__max']
            tornar_principal = tornar_principal or not imagens.filter(e_principal=True).exists()
            imagem = serializer.save(produto=produto, ordem=0 if ultima_ordem is None else ultima_ordem + 1)
            if tornar_principal:
                imagem.definir_como_principal()

    def perform_update(self, serializer):
        tornar_principal = serializer.validated_data.pop('e_principal', False)
        imagem = serializer.save()
        if tornar_principal:
            imagem.definir_como_principal()

    def perform_destroy(self, instance):
        instance.excluir()

    @action(detail=False, methods=['post'])
    def reordenar(self, request, produto_pk=None):
        imagens = list(self.get_queryset())
        nova_ordem = request.data.get('imagens')
        ids_validos = isinstance(nova_ordem, list) and all(type(imagem_id) is int for imagem_id in nova_ordem)

        if not ids_validos or sorted(nova_ordem) != sorted(imagem.id for imagem in imagens):
            raise serializers.ValidationError({'imagens': 'Envie a lista com todas as imagens do produto, na nova ordem.'})

        posicoes = {imagem_id: posicao for posicao, imagem_id in enumerate(nova_ordem)}
        for imagem in imagens:
            imagem.ordem = posicoes[imagem.id]
        ImagemProduto.objects.bulk_update(imagens, ['ordem'])

        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
