/**
 * avaliacoesService.js
 * Suporta dois modos controlados por VITE_USE_MOCK:
 *   true  → usa avaliacoes.json local (sem backend)
 *   false → usa API real (JWT injetado pelo apiClient)
 */

import { ref, computed } from 'vue'
import { api } from './apiClient.js'
import avaliacoesIniciais from '@/data/avaliacoes.json'

const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'

// ── Store local ───────────────────────────────────────────────
export const avaliacoesStore = ref(
  USE_MOCK ? [...avaliacoesIniciais] : []
)

// ── Listar comentários de um local ────────────────────────────
export async function listarComentarios(localId) {
  if (USE_MOCK) {
    return avaliacoesStore.value
      .filter(a => Number(a.localId) === Number(localId))
      .sort((a, b) => new Date(b.data) - new Date(a.data))
  }

  const data = await api.get(`/avaliacoes/local/${localId}`)
  // data = { estatisticas, avaliacoes }
  avaliacoesStore.value = data.avaliacoes
  return data.avaliacoes
}

// ── Estatísticas de um local ──────────────────────────────────
export async function estatisticasAvaliacoes(localId) {
  if (USE_MOCK) {
    const lista        = await listarComentarios(localId)
    const total        = lista.length
    const acessiveis   = lista.filter(a => a.acessivel).length
    const naoAcessiveis = total - acessiveis
    const percentualAcessivel = total > 0
      ? Math.round((acessiveis / total) * 100)
      : 0
    return { total, acessiveis, naoAcessiveis, percentualAcessivel }
  }

  const data = await api.get(`/avaliacoes/local/${localId}`)
  return data.estatisticas
}

// ── Enviar avaliação ──────────────────────────────────────────
export async function enviarAvaliacao(localId, acessivel, comentario, autor = 'Cidadão Anônimo', usuarioId = null) {
  if (USE_MOCK) {
    // Valida localmente
    if (!localId) throw new Error('localId é obrigatório.')
    if (typeof acessivel !== 'boolean') throw new Error('acessivel deve ser boolean.')
    if (!comentario || comentario.trim().length < 10)
      throw new Error('Comentário deve ter ao menos 10 caracteres.')

    const avaliacao = {
      id:         `aval-${Date.now()}`,
      localId:    Number(localId),
      acessivel,
      comentario: comentario.trim(),
      autor:      autor || 'Cidadão Anônimo',
      usuarioId:  usuarioId || null,
      data:       new Date().toISOString(),
    }
    avaliacoesStore.value = [avaliacao, ...avaliacoesStore.value]
    return { sucesso: true, avaliacao }
  }

  // API real — autor/usuarioId vêm do JWT, não precisam ser enviados
  const novaAvaliacao = await api.post('/avaliacoes', {
    local_id:   localId,
    acessivel,
    comentario,
  })
  avaliacoesStore.value = [novaAvaliacao, ...avaliacoesStore.value]
  return { sucesso: true, avaliacao: novaAvaliacao }
}

// ── Total geral ───────────────────────────────────────────────
export const totalAvaliacoes = computed(() => avaliacoesStore.value.length)