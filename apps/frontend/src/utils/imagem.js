// Recorte quadrado das imagens do produto, feito no navegador antes do envio.
// O enquadramento fica em pixels naturais da imagem: (cx, cy) é o centro do recorte e zoom >= 1,
// em que zoom 1 é o maior quadrado que cabe na imagem. Formato e tamanho continuam validados pelo backend.

export const ZOOM_MINIMO = 1
export const ZOOM_MAXIMO = 3
// Lado máximo da imagem gerada: suficiente para o detalhe do produto e bem abaixo do limite de 5 MB
const LADO_MAXIMO_SAIDA = 1200
const QUALIDADE_SAIDA = 0.9

// Imagens já salvas vêm de outro domínio (mídia do Django ou Supabase Storage). Baixá-las como blob evita que o
// canvas fique bloqueado por CORS ou reaproveite do cache uma resposta da miniatura sem cabeçalho CORS.
// Retorna sempre uma URL blob: que deve ser liberada com URL.revokeObjectURL por quem chamou.
export async function carregarImagemParaEdicao(src) {
  try {
    const resposta = await fetch(src, { mode: 'cors', cache: 'no-store' })
    if (!resposta.ok) throw new Error(`HTTP ${resposta.status}`)
    return URL.createObjectURL(await resposta.blob())
  } catch {
    throw new Error('Não foi possível abrir esta imagem para ajuste. Remova-a e envie novamente.')
  }
}

export function enquadramentoCentral(largura, altura) {
  return { cx: largura / 2, cy: altura / 2, zoom: ZOOM_MINIMO }
}

export function ladoDoRecorte(largura, altura, zoom) {
  return Math.min(largura, altura) / zoom
}

// Mantém o quadrado sempre dentro da imagem
export function limitarEnquadramento({ cx, cy, zoom }, largura, altura) {
  const zoomLimitado = Math.min(ZOOM_MAXIMO, Math.max(ZOOM_MINIMO, zoom))
  const metade = ladoDoRecorte(largura, altura, zoomLimitado) / 2
  return {
    cx: Math.min(largura - metade, Math.max(metade, cx)),
    cy: Math.min(altura - metade, Math.max(metade, cy)),
    zoom: zoomLimitado,
  }
}

export async function recortarQuadrado(elementoImagem, enquadramento, nomeOriginal = 'imagem') {
  const largura = elementoImagem.naturalWidth
  const altura = elementoImagem.naturalHeight
  const { cx, cy, zoom } = limitarEnquadramento(enquadramento, largura, altura)
  const lado = ladoDoRecorte(largura, altura, zoom)
  const ladoSaida = Math.max(1, Math.round(Math.min(lado, LADO_MAXIMO_SAIDA)))

  const canvas = document.createElement('canvas')
  canvas.width = ladoSaida
  canvas.height = ladoSaida
  const contexto = canvas.getContext('2d')
  contexto.imageSmoothingQuality = 'high'
  const desenhar = () => contexto.drawImage(elementoImagem, cx - lado / 2, cy - lado / 2, lado, lado, 0, 0, ladoSaida, ladoSaida)

  desenhar()
  let blob = await gerarBlob(canvas, 'image/webp')
  // Navegadores sem codificador WEBP devolvem PNG; nesse caso usa JPEG com fundo branco no lugar da transparência
  if (blob?.type !== 'image/webp') {
    contexto.fillStyle = 'white'
    contexto.fillRect(0, 0, ladoSaida, ladoSaida)
    desenhar()
    blob = await gerarBlob(canvas, 'image/jpeg')
  }
  if (!blob) throw new Error('Não foi possível gerar a imagem ajustada.')

  const extensao = blob.type === 'image/webp' ? 'webp' : 'jpg'
  const nomeBase = nomeOriginal.replace(/\.[^.]+$/, '') || 'imagem'
  return new File([blob], `${nomeBase}-quadrada.${extensao}`, { type: blob.type })
}

function gerarBlob(canvas, tipo) {
  return new Promise(resolver => canvas.toBlob(resolver, tipo, QUALIDADE_SAIDA))
}
