/**
 * acessibilidadeService.js
 * Serviço responsável por carregar, filtrar e classificar
 * os dados de acessibilidade dos locais de Teresina.
 * Inclui também as funções de Contribuição Cidadã.
 */

import { ref } from 'vue'
import locaisData from '@/data/locais.json'
import avaliacoesIniciais from '@/data/avaliacoes.json'

// ── STORE REATIVO para avaliações ────────────────────────────
// ref() do Vue: qualquer componente que usa este array via
// computed/watch é notificado automaticamente ao adicionar itens.
export const avaliacoesStore = ref([...avaliacoesIniciais])

/**
 * Envia uma avaliação cidadã para um local.
 *
 * @param {number}  localId
 * @param {boolean} acessivel
 * @param {string}  comentario
 * @param {string}  [autor]
 * @returns {{ sucesso: boolean, avaliacao: Object }}
 */
export function enviarAvaliacao(localId, acessivel, comentario, autor = 'Cidadão Anônimo') {
  if (!localId) throw new Error('localId é obrigatório.')
  if (typeof acessivel !== 'boolean') throw new Error('acessivel deve ser boolean.')
  if (!comentario || comentario.trim().length < 10)
    throw new Error('Comentário deve ter ao menos 10 caracteres.')
  if (comentario.trim().length > 500)
    throw new Error('Comentário deve ter no máximo 500 caracteres.')

  const avaliacao = {
    id: `aval-${Date.now()}`,
    localId: Number(localId),
    acessivel,
    comentario: comentario.trim(),
    autor: autor.trim() || 'Cidadão Anônimo',
    data: new Date().toISOString()
  }

  // unshift reativo: substitui o array para garantir detecção de mudança
  avaliacoesStore.value = [avaliacao, ...avaliacoesStore.value]

  return { sucesso: true, avaliacao }
}

/**
 * Lista avaliações de um local, ordenadas da mais recente.
 * @param {number} localId
 * @returns {Array}
 */
export function listarComentarios(localId) {
  return avaliacoesStore.value
    .filter(a => a.localId === Number(localId))
    .sort((a, b) => new Date(b.data) - new Date(a.data))
}

/**
 * Estatísticas agregadas das avaliações de um local.
 * @param {number} localId
 * @returns {{ total, acessiveis, naoAcessiveis, percentualAcessivel }}
 */
export function estatisticasAvaliacoes(localId) {
  const lista = listarComentarios(localId)
  const total = lista.length
  const acessiveis = lista.filter(a => a.acessivel).length
  const naoAcessiveis = total - acessiveis
  const percentualAcessivel = total > 0 ? Math.round((acessiveis / total) * 100) : null
  return { total, acessiveis, naoAcessiveis, percentualAcessivel }
}

/**
 * Locais com maior número de avaliações.
 * @param {number} limite
 * @returns {Array}
 */
export function locaisMaisAvaliados(limite = 5) {
  const contagem = {}
  avaliacoesStore.value.forEach(a => {
    contagem[a.localId] = (contagem[a.localId] || 0) + 1
  })
  return Object.entries(contagem)
    .sort(([, a], [, b]) => b - a)
    .slice(0, limite)
    .map(([localId, total]) => ({ local: getLocalById(Number(localId)), total }))
    .filter(item => item.local !== null)
}

// ─────────────────────────────────────────────────────────────
// FUNÇÕES DE LOCAIS
// ─────────────────────────────────────────────────────────────

export function classificarAcessibilidade(acessibilidade) {
  const campos = ['rampa','banheiroAdaptado','vagaPCD','elevador','entradaAcessivel','calcadaAcessivel']
  const score = campos.reduce((acc, campo) => acc + (acessibilidade[campo] ? 1 : 0), 0)
  const total = campos.length
  const percentual = score / total
  let nivel, label
  if (percentual >= 0.83)      { nivel = 'total';   label = 'Totalmente Acessível' }
  else if (percentual >= 0.33) { nivel = 'parcial'; label = 'Parcialmente Acessível' }
  else                         { nivel = 'nao';     label = 'Não Acessível' }
  return { nivel, label, score, total }
}

export function getLocais() {
  return locaisData.map(local => ({
    ...local,
    classificacao: classificarAcessibilidade(local.acessibilidade)
  }))
}

export function getLocalById(id) {
  const local = locaisData.find(l => l.id === Number(id))
  if (!local) return null
  return { ...local, classificacao: classificarAcessibilidade(local.acessibilidade) }
}

export function filtrarPorBusca(locais, query) {
  if (!query || query.trim() === '') return locais
  const q = query.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
  return locais.filter(l =>
    [l.nome, l.endereco, l.bairro, l.tipoLabel].some(c =>
      c.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').includes(q)
    )
  )
}

export function filtrarPorAcessibilidade(locais, filtros) {
  const ativos = Object.entries(filtros).filter(([, v]) => v).map(([k]) => k)
  if (ativos.length === 0) return locais
  return locais.filter(local => ativos.every(r => local.acessibilidade[r] === true))
}

export function filtrarPorNivel(locais, niveis) {
  if (!niveis || niveis.length === 0) return locais
  return locais.filter(l => niveis.includes(l.classificacao.nivel))
}

export const RECURSOS_META = {
  rampa:            { label: 'Rampa de Acesso',   icone: '♿',  descricao: 'Possui rampa para acesso de cadeirantes' },
  banheiroAdaptado: { label: 'Banheiro Adaptado', icone: '🚻', descricao: 'Possui banheiro com adaptações para PCD' },
  vagaPCD:          { label: 'Vaga PCD',          icone: '🅿️', descricao: 'Possui vagas reservadas para PCD no estacionamento' },
  elevador:         { label: 'Elevador',          icone: '🛗', descricao: 'Possui elevador acessível' },
  entradaAcessivel: { label: 'Entrada Acessível', icone: '🚪', descricao: 'Entrada principal sem barreiras arquitetônicas' },
  calcadaAcessivel: { label: 'Calçada Acessível', icone: '🛤️', descricao: 'Calçadas do entorno com piso regular e piso tátil' }
}

export const TIPOS_META = {
  shopping:        'Shopping Center',
  hospital:        'Hospital / UPA',
  educacao:        'Instituição de Ensino',
  servico_publico: 'Serviço Público',
  espaco_publico:  'Praça / Parque',
  banco:           'Agência Bancária',
  mercado:         'Mercado / Feira',
  cultura:         'Cultura e Lazer',
  transporte:      'Terminal / Transporte',
  supermercado:    'Supermercado',
  esporte:         'Complexo Esportivo'
}