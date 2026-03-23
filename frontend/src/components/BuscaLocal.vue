<template>
  <div class="busca-local">
    <!--
      role="search" identifica a região de busca para leitores de tela.
      É uma landmark region navegável por atalho (WCAG 2.4.1).
    -->
    <div role="search" class="busca-local__form">

      <!-- Label visível ou sr-only conforme prop -->
      <label
        :for="inputId"
        class="busca-local__label"
        :class="{ 'sr-only': labelOculto }"
      >
        {{ label }}
      </label>

      <div class="busca-local__input-wrapper">
        <!-- Ícone decorativo — aria-hidden pois o label já descreve (WCAG 1.1.1) -->
        <span class="busca-local__icon" aria-hidden="true">🔍</span>

        <input
          :id="inputId"
          ref="inputRef"
          v-model="query"
          type="search"
          class="br-input busca-local__input"
          :placeholder="placeholder"
          autocomplete="off"
          autocorrect="off"
          autocapitalize="off"
          spellcheck="false"
          :aria-label="label"
          :aria-describedby="query ? `${inputId}-results` : undefined"
          :aria-controls="mostrarSugestoes ? `${inputId}-listbox` : undefined"
          :aria-expanded="mostrarSugestoes"
          :aria-activedescendant="activeSugestaoId"
          role="combobox"
          aria-haspopup="listbox"
          aria-autocomplete="list"
          @input="onInput"
          @keydown="onKeydown"
          @blur="onBlur"
          @focus="onFocus"
        />

        <!-- Botão limpar — aparece apenas quando há texto -->
        <button
          v-if="query"
          class="busca-local__clear br-button tertiary"
          type="button"
          aria-label="Limpar busca"
          @click="limpar"
        >
          <span aria-hidden="true">✕</span>
        </button>
      </div>

      <!-- Lista de sugestões (combobox listbox) -->
      <ul
        v-if="mostrarSugestoes && sugestoes.length > 0"
        :id="`${inputId}-listbox`"
        role="listbox"
        :aria-label="`Sugestões para: ${query}`"
        class="busca-local__sugestoes"
      >
        <li
          v-for="(sugestao, index) in sugestoes"
          :key="sugestao.id"
          :id="`${inputId}-option-${index}`"
          role="option"
          :aria-selected="activeSugestaoIndex === index"
          class="busca-local__sugestao"
          :class="{ 'is-active': activeSugestaoIndex === index }"
          @mousedown.prevent="selecionarSugestao(sugestao)"
        >
          <span class="busca-local__sugestao-nome">{{ sugestao.nome }}</span>
          <span class="busca-local__sugestao-meta">
            {{ sugestao.tipoLabel }} — {{ sugestao.bairro }}
          </span>
        </li>
      </ul>

      <!-- Mensagem de nenhum resultado -->
      <div
        v-if="mostrarSemResultado"
        role="status"
        aria-live="polite"
        class="busca-local__vazio"
      >
        Nenhum local encontrado para "{{ query }}"
      </div>

      <!-- Contador de resultados para leitores de tela -->
      <div
        v-if="query && !mostrarSugestoes"
        :id="`${inputId}-results`"
        aria-live="polite"
        aria-atomic="true"
        class="sr-only"
      >
        {{ resultCount }} resultado{{ resultCount !== 1 ? 's' : '' }} encontrado{{ resultCount !== 1 ? 's' : '' }}
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { filtrarPorBusca } from '@/services/acessibilidadeService.js'
import { getLocais } from '@/services/acessibilidadeService.js'

const props = defineProps({
  label: { type: String, default: 'Buscar local em Teresina' },
  placeholder: { type: String, default: 'Ex.: Shopping Rio Poty, Hospital, Praça...' },
  labelOculto: { type: Boolean, default: false },
  /** Máximo de sugestões exibidas no dropdown */
  maxSugestoes: { type: Number, default: 6 }
})

const emit = defineEmits(['select', 'search'])

// ID único para acessibilidade (evita conflitos quando há múltiplos componentes)
const inputId = `busca-${Math.random().toString(36).slice(2, 8)}`

const inputRef = ref(null)
const query = ref('')
const isFocused = ref(false)
const activeSugestaoIndex = ref(-1)

const todosLocais = ref([])

/** Sugestões filtradas com base no query atual */
const sugestoes = computed(() => {
  if (!query.value || query.value.trim().length < 2) return []
  return filtrarPorBusca(todosLocais, query.value).slice(0, props.maxSugestoes)
})

const mostrarSugestoes = computed(
  () => isFocused.value && sugestoes.value.length > 0
)

const mostrarSemResultado = computed(
  () => isFocused.value && query.value.trim().length >= 2 && sugestoes.value.length === 0
)

const resultCount = computed(() => sugestoes.value.length)

/** ID do item ativo no listbox para aria-activedescendant */
const activeSugestaoId = computed(() => {
  if (activeSugestaoIndex.value < 0) return undefined
  return `${inputId}-option-${activeSugestaoIndex.value}`
})

function onInput() {
  activeSugestaoIndex.value = -1
  emit('search', query.value)
}

function onFocus() {
  isFocused.value = true
}

function onBlur() {
  // Pequeno delay para permitir o click nas sugestões (mousedown.prevent previne o blur)
  setTimeout(() => { isFocused.value = false }, 150)
}

/**
 * Navegação por teclado no combobox (WCAG 2.1.1).
 * ↑/↓ navegam nas sugestões.
 * Enter seleciona ou busca.
 * Escape fecha o listbox.
 */
function onKeydown(e) {
  if (!mostrarSugestoes.value) return

  switch (e.key) {
    case 'ArrowDown':
      e.preventDefault()
      activeSugestaoIndex.value = Math.min(
        activeSugestaoIndex.value + 1,
        sugestoes.value.length - 1
      )
      break
    case 'ArrowUp':
      e.preventDefault()
      activeSugestaoIndex.value = Math.max(activeSugestaoIndex.value - 1, -1)
      break
    case 'Enter':
      e.preventDefault()
      if (activeSugestaoIndex.value >= 0) {
        selecionarSugestao(sugestoes.value[activeSugestaoIndex.value])
      } else {
        emit('search', query.value)
        isFocused.value = false
      }
      break
    case 'Escape':
      isFocused.value = false
      activeSugestaoIndex.value = -1
      break
  }
}

function selecionarSugestao(sugestao) {
  query.value = sugestao.nome
  isFocused.value = false
  activeSugestaoIndex.value = -1
  emit('select', sugestao)
}

function limpar() {
  query.value = ''
  emit('search', '')
  inputRef.value?.focus()
}

// Expõe o método focus para uso externo (ex: skip link)
defineExpose({ focus: () => inputRef.value?.focus() })
</script>

<style scoped>
.busca-local { position: relative; width: 100%; }

.busca-local__form { position: relative; }

.busca-local__label {
  display: block;
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  margin-bottom: var(--space-2);
}

.busca-local__input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.busca-local__icon {
  position: absolute;
  left: var(--space-4);
  font-size: 1rem;
  pointer-events: none;
  z-index: 1;
}

.busca-local__input {
  padding-left: 2.75rem;
  padding-right: 2.75rem;
  font-size: var(--font-size-md);
}

.busca-local__clear {
  position: absolute;
  right: var(--space-2);
  padding: var(--space-1) var(--space-2) !important;
  min-height: unset !important;
  color: var(--color-gray-60) !important;
  font-size: var(--font-size-sm);
}

/* Listbox de sugestões */
.busca-local__sugestoes {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  z-index: 200;
  list-style: none;
  background: var(--color-white);
  border: 1px solid var(--color-gray-20);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  max-height: 320px;
  overflow-y: auto;
  padding: var(--space-1) 0;
}

.busca-local__sugestao {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: var(--space-3) var(--space-4);
  cursor: pointer;
  border-bottom: 1px solid var(--color-gray-10);
  transition: background var(--transition-fast);
}
.busca-local__sugestao:last-child { border-bottom: none; }
.busca-local__sugestao:hover,
.busca-local__sugestao.is-active {
  background: var(--color-primary-lightest);
}

.busca-local__sugestao-nome {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
}
.busca-local__sugestao-meta {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
}

.busca-local__vazio {
  position: absolute;
  top: calc(100% + 4px);
  left: 0; right: 0;
  z-index: 200;
  background: var(--color-white);
  border: 1px solid var(--color-gray-20);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  box-shadow: var(--shadow-sm);
}
</style>