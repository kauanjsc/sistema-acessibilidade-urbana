<template>
  <!--
    role="img" com aria-label descreve o badge para leitores de tela
    como se fosse uma imagem com significado (WCAG 1.1.1).
    Não usamos apenas cor para transmitir a informação (WCAG 1.4.1).
  -->
  <span
    class="badge-acessibilidade"
    :class="nivel"
    role="img"
    :aria-label="`Nível de acessibilidade: ${label}`"
  >
    <component :is="icone" aria-hidden="true" :size="16" style="margin-right: 4px; vertical-align: text-bottom;" />
    <span>{{ label }}</span>
    <span v-if="mostrarScore" class="badge-score" aria-hidden="true">
      {{ score }}/{{ total }}
    </span>
  </span>
</template>

<script setup>
import { computed } from 'vue'
import { CheckCircle, TriangleAlert, XCircle, HelpCircle } from 'lucide-vue-next'

const props = defineProps({
  /** 'total' | 'parcial' | 'nao' */
  nivel: {
    type: String,
    required: true,
    validator: v => ['total', 'parcial', 'nao'].includes(v)
  },
  label: {
    type: String,
    required: true
  },
  score: {
    type: Number,
    default: null
  },
  total: {
    type: Number,
    default: 6
  },
  /** Se true, exibe o score numérico (ex: 5/6) */
  mostrarScore: {
    type: Boolean,
    default: false
  }
})

const icone = computed(() => {
  const icones = {
    total: CheckCircle,
    parcial: TriangleAlert,
    nao:     XCircle
  }
  return icones[props.nivel] || HelpCircle
})
</script>

<style scoped>
.badge-score {
  font-weight: var(--font-weight-regular);
  opacity: 0.8;
}
</style>