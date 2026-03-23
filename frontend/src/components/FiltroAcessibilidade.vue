<template>
  <!--
    <section> com aria-label nomeia esta região para leitores de tela.
    fieldset/legend é a abordagem semântica correta para grupos de checkboxes (WCAG 1.3.1).
  -->
  <section class="filtro-panel" aria-label="Filtros de acessibilidade">

    <div class="filtro-panel__header">
      <h2 class="filtro-panel__title" id="filtro-heading">
        <component :is="lucideIcons.Search" :size="20" aria-hidden="true" style="margin-right: 8px; vertical-align: middle;" />
        Filtros
      </h2>

      <!-- Contador de filtros ativos -->
      <span
        v-if="totalAtivos > 0"
        class="filtro-panel__badge"
        :aria-label="`${totalAtivos} filtro${totalAtivos !== 1 ? 's' : ''} ativo${totalAtivos !== 1 ? 's' : ''}`"
      >
        {{ totalAtivos }}
      </span>

      <button
        v-if="totalAtivos > 0"
        class="filtro-panel__limpar br-button tertiary"
        type="button"
        @click="limparFiltros"
      >
        Limpar
      </button>
    </div>

    <!-- Grupo 1: Recursos de acessibilidade -->
    <fieldset class="filtro-panel__fieldset">
      <legend class="filtro-panel__legend">Recursos de acessibilidade</legend>

      <div class="filtro-panel__lista">
        <label
          v-for="recurso in recursos"
          :key="recurso.chave"
          class="br-checkbox filtro-panel__item"
          :for="`filtro-${recurso.chave}`"
        >
          <input
            :id="`filtro-${recurso.chave}`"
            v-model="filtrosRecursos[recurso.chave]"
            type="checkbox"
            :aria-describedby="`filtro-desc-${recurso.chave}`"
            @change="emitirFiltros"
          />
          <span class="filtro-panel__item-label">
            <component
              :is="lucideIcons[recurso.icone]"
              :size="16"
              stroke-width="2"
              aria-hidden="true"
              class="icone-recurso"
            />
            {{ recurso.label }}
          </span>
          <!-- Descrição extra para leitores de tela (WCAG 1.3.3) -->
          <span
            :id="`filtro-desc-${recurso.chave}`"
            class="sr-only"
          >
            {{ recurso.descricao }}
          </span>
        </label>
      </div>
    </fieldset>

    <hr class="divider" />

    <!-- Grupo 2: Nível de acessibilidade -->
    <fieldset class="filtro-panel__fieldset">
      <legend class="filtro-panel__legend">Nível de acessibilidade</legend>

      <div class="filtro-panel__lista">
        <label
          v-for="nivel in niveis"
          :key="nivel.valor"
          class="br-checkbox filtro-panel__item"
          :for="`nivel-${nivel.valor}`"
        >
          <input
            :id="`nivel-${nivel.valor}`"
            v-model="filtrosNiveis[nivel.valor]"
            type="checkbox"
            @change="emitirFiltros"
          />
          <span class="filtro-panel__item-label">
            <span
              class="filtro-panel__nivel-dot"
              :class="`dot-${nivel.valor}`"
              aria-hidden="true"
            ></span>
            {{ nivel.label }}
          </span>
        </label>
      </div>
    </fieldset>

    <!-- Live region para anunciar mudanças nos filtros -->
    <div
      aria-live="polite"
      aria-atomic="true"
      class="sr-only"
      role="status"
    >
      {{ anuncioFiltro }}
    </div>

  </section>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { RECURSOS_META } from '@/services/acessibilidadeService.js'
import * as lucideIcons from 'lucide-vue-next'

const emit = defineEmits(['change'])

// ── Recursos de acessibilidade ──────────────────────────────
const recursos = Object.entries(RECURSOS_META).map(([chave, meta]) => ({
  chave,
  ...meta
}))

const filtrosRecursos = ref(
  Object.fromEntries(recursos.map(r => [r.chave, false]))
)

// ── Níveis de acessibilidade ────────────────────────────────
const niveis = [
  { valor: 'total',   label: 'Totalmente Acessível' },
  { valor: 'parcial', label: 'Parcialmente Acessível' },
  { valor: 'nao',     label: 'Não Acessível' }
]

const filtrosNiveis = ref(
  Object.fromEntries(niveis.map(n => [n.valor, false]))
)

// ── Contador de filtros ativos ──────────────────────────────
const totalAtivos = computed(() => {
  const recursos = Object.values(filtrosRecursos.value).filter(Boolean).length
  const niveis = Object.values(filtrosNiveis.value).filter(Boolean).length
  return recursos + niveis
})

// ── Anúncio para leitores de tela ───────────────────────────
const anuncioFiltro = ref('')

function emitirFiltros() {
  const recursosAtivos = Object.fromEntries(
    Object.entries(filtrosRecursos.value).filter(([, v]) => v)
  )
  const niveisAtivos = Object.entries(filtrosNiveis.value)
    .filter(([, v]) => v)
    .map(([k]) => k)

  emit('change', { recursos: recursosAtivos, niveis: niveisAtivos })

  anuncioFiltro.value = totalAtivos.value > 0
    ? `${totalAtivos.value} filtro${totalAtivos.value !== 1 ? 's' : ''} ativo${totalAtivos.value !== 1 ? 's' : ''}`
    : 'Todos os filtros removidos'
}

function limparFiltros() {
  recursos.forEach(r => { filtrosRecursos.value[r.chave] = false })
  niveis.forEach(n => { filtrosNiveis.value[n.valor] = false })
  emitirFiltros()
}
</script>

<style scoped>
.icone-recurso {
  color: var(--color-primary-default);
  flex-shrink: 0;
}

.br-checkbox input + .filtro-panel__item-label {
  margin-left: var(--space-1);
}
.filtro-panel {
  background: var(--color-surface);
  border: 1px solid var(--color-gray-10);
  border-radius: var(--radius-md);
  padding: var(--space-6);
  box-shadow: var(--shadow-sm);
}

.filtro-panel__header {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-4);
}

.filtro-panel__title {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-bold);
  color: var(--color-primary-default);
  flex: 1;
}

.filtro-panel__badge {
  background: var(--color-primary-default);
  color: var(--color-white);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  padding: 2px var(--space-2);
  border-radius: var(--radius-full);
  min-width: 20px;
  text-align: center;
}

.filtro-panel__limpar {
  font-size: var(--font-size-xs) !important;
  padding: var(--space-1) var(--space-3) !important;
  min-height: unset !important;
  color: var(--color-danger) !important;
}

/* Fieldset reset */
.filtro-panel__fieldset {
  border: none;
  padding: 0;
  margin: 0;
}

.filtro-panel__legend {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: var(--space-3);
  float: left;
  width: 100%;
}

.filtro-panel__lista {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  clear: both;
}

.filtro-panel__item {
  padding: var(--space-2) var(--space-2);
  border-radius: var(--radius-sm);
  transition: background var(--transition-fast);
}
.filtro-panel__item:hover {
  background: var(--color-gray-05);
}

.filtro-panel__item-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

/* Pontos coloridos de nível */
.filtro-panel__nivel-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}
.dot-total   { background: var(--color-accessible-green); }
.dot-parcial { background: var(--color-warning-dark); }
.dot-nao     { background: var(--color-accessible-red); }
</style>