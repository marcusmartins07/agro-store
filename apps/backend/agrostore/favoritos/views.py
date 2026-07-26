from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Favorito
from .serializers import FavoritoSerializer


class FavoritoViewSet(viewsets.ModelViewSet):
    serializer_class = FavoritoSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_queryset(self):
        return Favorito.objects.filter(
            usuario=self.request.user
        ).select_related('produto', 'produto__loja')

    def perform_create(self, serializer):
        usuario = self.request.user
        produto = serializer.validated_data['produto']

        # Se já favoritado, retorna sem duplicar
        if Favorito.objects.filter(usuario=usuario, produto=produto).exists():
            raise serializers.ValidationError("Produto já está nos favoritos.")

        serializer.save(usuario=usuario)