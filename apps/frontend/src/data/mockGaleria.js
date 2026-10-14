// MOCK: o backend guarda no máximo uma imagem por produto (regra de negócio v1, campo Produto.imagem).
// Os slides "ilustrativos" existem só no frontend, para demonstrar o carrossel do protótipo.
// Quando houver um endpoint com várias imagens por produto, troque esta função pela lista vinda da API.

const QUANTIDADE_SLIDES_ILUSTRATIVOS = 2

export function montarGaleriaProduto(produto) {
  const slidePrincipal = produto.imagem
    ? { tipo: 'imagem', src: produto.imagem, alt: produto.nome }
    : { tipo: 'sem-foto', alt: `${produto.nome} sem foto cadastrada` }

  const slidesIlustrativos = Array.from({ length: QUANTIDADE_SLIDES_ILUSTRATIVOS }, () => ({
    tipo: 'ilustrativa',
    alt: 'Imagem ilustrativa',
  }))

  return [slidePrincipal, ...slidesIlustrativos]
}
