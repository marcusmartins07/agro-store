from django.db import IntegrityError, transaction
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from agrostore.main.imagens import nome_gerenciado
from .models import Loja
from .serializers import PASTA_IMAGEM_LOJA, LojaSerializer, remover_imagem_loja_apos_commit


MENSAGEM_SEM_LOJA = "Você não possui uma loja cadastrada."


class LojaViewSet(viewsets.ModelViewSet):
    queryset = Loja.objects.select_related('proprietario').all()
    serializer_class = LojaSerializer
    http_method_names = ['get', 'post']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        # RN-013: em pedidos simultâneos, a validação do serializer passa nos dois e o banco recusa o segundo.
        try:
            with transaction.atomic():
                serializer.save(proprietario=self.request.user)
        except IntegrityError:
            if not Loja.objects.filter(proprietario=self.request.user).exists():
                raise
            raise serializers.ValidationError(
                {api_settings.NON_FIELD_ERRORS_KEY: ["Cada produtor pode possuir somente uma loja."]}
            )


class MinhaLojaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        loja = Loja.objects.filter(proprietario=request.user).first()

        if not loja:
            return Response({"detail": MENSAGEM_SEM_LOJA}, status=404)

        serializer = LojaSerializer(loja, context={'request': request})
        return Response(serializer.data)

    def patch(self, request):
        loja = Loja.objects.filter(proprietario=request.user).first()
        if not loja:
            return Response({"detail": MENSAGEM_SEM_LOJA}, status=status.HTTP_404_NOT_FOUND)

        campos_permitidos = {'nome', 'descricao', 'ativa', 'imagem_perfil'}
        campos_enviados = set(request.data.keys())
        campos_invalidos = campos_enviados - campos_permitidos
        if campos_invalidos:
            return Response(
                {"detail": "Somente nome, descrição, imagem e status da loja podem ser alterados nesta área."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = LojaSerializer(loja, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(LojaSerializer(serializer.save(), context={'request': request}).data)


class MinhaLojaImagemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        loja = Loja.objects.filter(proprietario=request.user).first()
        if not loja:
            return Response({"detail": MENSAGEM_SEM_LOJA}, status=status.HTTP_404_NOT_FOUND)

        nome_anterior = loja.imagem_perfil.name
        # Valor vazio ou fora do padrão gerado é exibido como sem imagem; o dado legado é preservado.
        if not nome_gerenciado(nome_anterior, PASTA_IMAGEM_LOJA):
            return Response({"detail": "A loja não possui imagem."}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            loja.imagem_perfil = ''
            loja.save(update_fields=['imagem_perfil', 'data_atualizacao'])
            remover_imagem_loja_apos_commit(loja, nome_anterior)
        return Response(status=status.HTTP_204_NO_CONTENT)
