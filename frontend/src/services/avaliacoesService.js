/**
 * avaliacoesService.js
 * Service dedicado ao gerenciamento de avaliações cidadãs.
 * Separado do acessibilidadeService para manter responsabilidades distintas.
 *
 * O store usa ref() do Vue: qualquer computed que leia
 * avaliacoesStore.value é atualizado automaticamente ao mudar.
 */

import { ref, computed } from 'vue'
import avaliacoesIniciais from '@/data/avaliacoes.json'

// ── Store reativo ─────────────────────────────────────────────
export const avaliacoesStore = ref([...avaliacoesIniciais])

// ── Enviar avaliação ─────────────────────────────────────────
export function enviarAvaliacao(localId, acessivel, comentario, autor = 'Cidadão Anônimo', usuarioId = null) {
  if (!localId)
    throw new Error('localId é obrigatório.')
  if (typeof acessivel !== 'boolean')
    throw new Error('acessivel deve ser boolean.')
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
    usuarioId: usuarioId || null,
    data: new Date().toISOString()
  }

  // Substitui o array inteiro — garante reatividade do Vue
  avaliacoesStore.value = [avaliacao, ...avaliacoesStore.value]

  return { sucesso: true, avaliacao }
}

// ── Listar comentários de um local ───────────────────────────
export function listarComentarios(localId) {
  return avaliacoesStore.value
    .filter(a => a.localId === Number(localId))
    .sort((a, b) => new Date(b.data) - new Date(a.data))
}

// ── Estatísticas de um local ─────────────────────────────────
export function estatisticasAvaliacoes(localId) {
  const lista = listarComentarios(localId)
  const total = lista.length
  const acessiveis = lista.filter(a => a.acessivel).length
  const naoAcessiveis = total - acessiveis
  const percentualAcessivel = total > 0 ? Math.round((acessiveis / total) * 100) : 0
  return { total, acessiveis, naoAcessiveis, percentualAcessivel }
}

// ── Total geral de avaliações (para stats da home/contribuir) ─
export const totalAvaliacoes = computed(() => avaliacoesStore.value.length)