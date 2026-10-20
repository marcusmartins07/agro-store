from django.utils import timezone

from .models import Carrinho, CarrinhoProduto


def ajustar_carrinhos_ao_estoque(produto):
    """Reduz ao estoque atual os itens de carrinho que passaram dele. A reposição não restaura a quantidade."""
    estoque = max(produto.estoque, 0)
    itens_acima_do_estoque = CarrinhoProduto.objects.filter(produto=produto, quantidade__gt=estoque)
    carrinho_ids = list(itens_acima_do_estoque.values_list('carrinho_id', flat=True))
    if not carrinho_ids:
        return

    itens_acima_do_estoque.update(quantidade=estoque, data_atualizacao=timezone.now())
    for carrinho in Carrinho.objects.filter(carrinho_id__in=carrinho_ids).order_by('carrinho_id'):
        carrinho.recalcular_totais()
