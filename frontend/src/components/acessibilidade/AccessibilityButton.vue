<template>
  <!--
    AccessibilityButton.vue
    Botão flutuante fixo no canto inferior direito.
    Única responsabilidade: abrir/fechar o painel via useAcessibilidade.
  -->
  <button
    class="a11y-btn"
    :class="{ 'a11y-btn--ativo': painelAberto }"
    type="button"
    role="button"
    tabindex="0"
    :aria-expanded="painelAberto"
    aria-controls="painel-acessibilidade"
    :aria-label="painelAberto
      ? 'Fechar ferramentas de acessibilidade'
      : 'Abrir ferramentas de acessibilidade'"
    :title="painelAberto ? 'Fechar' : 'Acessibilidade'"
    @click="togglePainel"
    @keydown.enter.prevent="togglePainel"
    @keydown.space.prevent="togglePainel"
  >
    <!-- Ícone universal de acessibilidade (ISA / ISO 7001) -->
    <svg
      class="a11y-btn__icone"
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
      focusable="false"
    >
      <!-- Cabeça -->
      <circle cx="12" cy="4.5" r="1.75" fill="currentColor" />
      <!-- Corpo / braços -->
      <path
        d="M12 7.5c-1 0-1.8.8-1.8 1.8V13l-1.8 3.6h1.4l.9-1.8h2.6l.9 1.8H15.6L13.8 13V9.3c0-1-.8-1.8-1.8-1.8z"
        fill="currentColor"
      />
      <!-- Pernas/cadeira de rodas estilizada -->
      <path
        d="M8.2 9.8C6.6 10.7 5.5 12.4 5.5 14.4c0 3.6 2.9 6.1 6.5 6.1s6.5-2.5 6.5-6.1c0-2-.9-3.7-2.3-4.8"
        stroke="currentColor"
        stroke-width="1.6"
        stroke-linecap="round"
        fill="none"
      />
    </svg>

    <!-- Badge com número de recursos ativos -->
    <span
      v-if="totalAtivos > 0"
      class="a11y-btn__badge"
      aria-hidden="true"
    >
      {{ totalAtivos }}
    </span>
  </button>
</template>

<script setup>
import { useAcessibilidade } from '@/services/useAcessibilidade.js'


const {
  painelAberto,
  totalAtivos,
  togglePainel,
} = useAcessibilidade()
</script>

<style scoped>
/* ── BOTÃO FLUTUANTE ─────────────────────────────────────────── */
.a11y-btn {
  /* Posicionamento fixo — requisito principal */
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9100;

  /* Dimensões e forma */
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: none;
  padding: 0;

  /* Visual Gov.br */
  background: var(--color-primary-default, #1351B4);
  color: var(--color-white, #fff);
  cursor: pointer;

  /* Layout interno */
  display: flex;
  align-items: center;
  justify-content: center;

  /* Sombra e transição */
  box-shadow:
    0 4px 16px rgba(19, 81, 180, 0.45),
    0 2px 6px rgba(0, 0, 0, 0.15);
  transition:
    background 150ms ease,
    transform  150ms ease,
    box-shadow 150ms ease;
}

/* Estado hover */
.a11y-btn:hover {
  background: var(--color-primary-dark, #0C326F);
  transform: scale(1.07);
  box-shadow:
    0 6px 20px rgba(19, 81, 180, 0.5),
    0 3px 8px rgba(0, 0, 0, 0.2);
}

/* Estado ativo (painel aberto) */
.a11y-btn--ativo {
  background: var(--color-primary-darker, #071D41);
  transform: scale(0.95);
}

/* Foco via teclado — WCAG 2.4.7 */
.a11y-btn:focus-visible {
  outline: 3px solid var(--color-border-focus, #C44601);
  outline-offset: 3px;
}

/* Clique / press */
.a11y-btn:active {
  transform: scale(0.93);
}

/* ── ÍCONE ───────────────────────────────────────────────────── */
.a11y-btn__icone {
  width: 28px;
  height: 28px;
  transition: transform 200ms ease;
  flex-shrink: 0;
}

.a11y-btn--ativo .a11y-btn__icone {
  transform: rotate(15deg) scale(0.9);
}

/* ── BADGE ───────────────────────────────────────────────────── */
.a11y-btn__badge {
  position: absolute;
  top: -3px;
  right: -3px;
  min-width: 20px;
  height: 20px;
  padding: 0 4px;
  border-radius: 999px;

  background: var(--color-warning, #FFCD07);
  color: var(--color-primary-darker, #071D41);
  font-size: 11px;
  font-weight: 800;
  line-height: 1;

  display: flex;
  align-items: center;
  justify-content: center;

  border: 2px solid var(--color-white, #fff);
  pointer-events: none;
}

/* ── REDUCED MOTION ──────────────────────────────────────────── */
@media (prefers-reduced-motion: reduce) {
  .a11y-btn,
  .a11y-btn__icone {
    transition: none;
  }
  .a11y-btn:hover  { transform: none; }
  .a11y-btn--ativo { transform: none; }
}
</style>