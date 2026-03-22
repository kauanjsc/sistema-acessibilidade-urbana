<template>
  <!--
    AccessibilityPanel.vue
    Painel flutuante com as opções de acessibilidade.
    Posicionado acima do AccessibilityButton, alinhado à direita.
    Única responsabilidade: apresentar e acionar as opções.
  -->
  <Transition name="painel">
    <div
      v-if="painelAberto"
      id="painel-acessibilidade"
      class="a11y-painel"
      role="dialog"
      aria-label="Opções de acessibilidade"
      aria-modal="false"
    >

      <!-- ── Cabeçalho ───────────────────────────────────────── -->
      <div class="a11y-painel__header">
        <div class="a11y-painel__header-titulo">
          <span class="a11y-painel__header-icone" aria-hidden="true">
            <svg viewBox="0 0 20 20" fill="none" aria-hidden="true" focusable="false">
              <circle cx="10" cy="10" r="9" stroke="currentColor" stroke-width="1.5"/>
              <path d="M10 1a9 9 0 0 1 0 18V1z" fill="currentColor"/>
            </svg>
          </span>
          <span>Acessibilidade</span>
        </div>
        <button
          class="a11y-painel__fechar"
          type="button"
          aria-label="Fechar painel de acessibilidade"
          @click="fecharPainel"
        >
          <svg viewBox="0 0 16 16" fill="none" aria-hidden="true" focusable="false">
            <path d="M2 2l12 12M14 2L2 14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </button>
      </div>

      <!-- ── TEMA ────────────────────────────────────────────── -->
      <section class="a11y-painel__secao" aria-labelledby="label-tema">
        <p id="label-tema" class="a11y-painel__secao-titulo">Tema</p>
        <div class="a11y-painel__tema-opcoes" role="group" aria-labelledby="label-tema">
          <button
            class="a11y-painel__tema-btn"
            :class="{ 'a11y-painel__tema-btn--ativo': !modoEscuro }"
            type="button"
            :aria-pressed="!modoEscuro"
            aria-label="Ativar tema claro"
            @click="setModoEscuro(false)"
          >
            <span class="a11y-painel__tema-icone" aria-hidden="true">☀️</span>
            <span class="a11y-painel__tema-texto">Claro</span>
          </button>

          <button
            class="a11y-painel__tema-btn"
            :class="{ 'a11y-painel__tema-btn--ativo': modoEscuro }"
            type="button"
            :aria-pressed="modoEscuro"
            aria-label="Ativar tema escuro"
            @click="setModoEscuro(true)"
          >
            <span class="a11y-painel__tema-icone" aria-hidden="true">🌙</span>
            <span class="a11y-painel__tema-texto">Escuro</span>
          </button>
        </div>
      </section>

      <!-- ── ALTO CONTRASTE ──────────────────────────────────── -->
      <section class="a11y-painel__secao" aria-labelledby="label-contraste">
        <p id="label-contraste" class="a11y-painel__secao-titulo">Contraste</p>
        <button
          class="a11y-painel__toggle"
          :class="{ 'a11y-painel__toggle--ativo': altoContraste }"
          type="button"
          :aria-pressed="altoContraste"
          aria-label="Alternar modo de alto contraste"
          @click="toggleAltoContraste"
        >
          <span class="a11y-painel__toggle-icone" aria-hidden="true">
            <svg viewBox="0 0 20 20" fill="none" aria-hidden="true" focusable="false">
              <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.5"/>
              <path d="M10 2a8 8 0 0 1 0 16V2z" fill="currentColor"/>
            </svg>
          </span>
          <span class="a11y-painel__toggle-corpo">
            <span class="a11y-painel__toggle-label">Alto contraste</span>
            <span class="a11y-painel__toggle-desc">Aumenta a legibilidade</span>
          </span>
          <span class="a11y-painel__toggle-pill" aria-hidden="true">
            {{ altoContraste ? 'ON' : 'OFF' }}
          </span>
        </button>
      </section>

      <!-- ── TAMANHO DA FONTE ────────────────────────────────── -->
      <section class="a11y-painel__secao" aria-labelledby="label-fonte">
        <p id="label-fonte" class="a11y-painel__secao-titulo">Tamanho do texto</p>
        <div class="a11y-painel__fonte-controle" role="group" aria-labelledby="label-fonte">
          <button
            class="a11y-painel__fonte-btn"
            type="button"
            :disabled="tamanhoFonte <= FONTE_MIN"
            aria-label="Diminuir tamanho do texto"
            @click="ajustarFonte(-1)"
          >
            <span aria-hidden="true">A<sub>−</sub></span>
          </button>

          <div
            class="a11y-painel__fonte-dots"
            role="status"
            :aria-label="`Fonte ${tamanhoFonte}px — ${fonteLabel}`"
          >
            <span
              v-for="n in (FONTE_MAX - FONTE_MIN) / 2 + 1"
              :key="n"
              class="a11y-painel__fonte-dot"
              :class="{ 'a11y-painel__fonte-dot--ativo': FONTE_MIN + (n - 1) * 2 <= tamanhoFonte }"
              aria-hidden="true"
            />
          </div>

          <button
            class="a11y-painel__fonte-btn"
            type="button"
            :disabled="tamanhoFonte >= FONTE_MAX"
            aria-label="Aumentar tamanho do texto"
            @click="ajustarFonte(+1)"
          >
            <span aria-hidden="true">A<sup>+</sup></span>
          </button>
        </div>
        <p class="a11y-painel__fonte-label" aria-live="polite">{{ fonteLabel }}</p>
      </section>

      <!-- ── NAVEGAÇÃO POR TECLADO ───────────────────────────── -->
      <section class="a11y-painel__secao" aria-labelledby="label-teclado">
        <p id="label-teclado" class="a11y-painel__secao-titulo">Navegação</p>
        <button
          class="a11y-painel__toggle"
          :class="{ 'a11y-painel__toggle--ativo': navegacaoTeclado }"
          type="button"
          :aria-pressed="navegacaoTeclado"
          aria-label="Alternar destaque de foco para navegação por teclado"
          @click="toggleNavTeclado"
        >
          <span class="a11y-painel__toggle-icone" aria-hidden="true">
            <svg viewBox="0 0 20 20" fill="none" aria-hidden="true" focusable="false">
              <rect x="1" y="5" width="18" height="12" rx="2" stroke="currentColor" stroke-width="1.5"/>
              <path d="M4 9h2M8 9h2M12 9h2M4 13h12M16 9h0" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </span>
          <span class="a11y-painel__toggle-corpo">
            <span class="a11y-painel__toggle-label">Foco visível (TAB)</span>
            <span class="a11y-painel__toggle-desc">Realça elementos focáveis</span>
          </span>
          <span class="a11y-painel__toggle-pill" aria-hidden="true">
            {{ navegacaoTeclado ? 'ON' : 'OFF' }}
          </span>
        </button>
      </section>


            <!-- ── RESTAURAR ───────────────────────────────────────── -->
      <div class="a11y-painel__rodape">
        <button
          class="a11y-painel__resetar"
          type="button"
          aria-label="Restaurar todas as configurações de acessibilidade ao padrão"
          @click="resetarTudo"
        >
          <svg viewBox="0 0 16 16" fill="none" aria-hidden="true" focusable="false" style="width:14px;height:14px;">
            <path d="M13.5 8A5.5 5.5 0 1 1 8 2.5a5.5 5.5 0 0 1 3.9 1.6L14 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          Restaurar padrão
        </button>
      </div>

    </div>
  </Transition>
</template>

<script setup>
import { computed } from 'vue'
import { useAcessibilidade } from '@/services/useAcessibilidade.js'

const {
  painelAberto,
  modoEscuro,
  altoContraste,
  tamanhoFonte,
  navegacaoTeclado,
  FONTE_BASE,
  FONTE_MIN,
  FONTE_MAX,
  fecharPainel,
  setModoEscuro,
  toggleAltoContraste,
  ajustarFonte,
  toggleNavTeclado,
  resetarTudo,
} = useAcessibilidade()

const fonteLabel = computed(() => {
  if (tamanhoFonte.value === FONTE_BASE) return 'Padrão (16 px)'
  const pct = Math.round((tamanhoFonte.value / FONTE_BASE) * 100)
  return `${pct}% do tamanho padrão`
})
</script>

<style scoped>
/* ── PAINEL CONTAINER ────────────────────────────────────────── */
.a11y-painel {
  position: fixed;
  bottom: 88px;   /* empilhado acima do botão (56px + 20px base + 12px gap) */
  right: 20px;
  z-index: 9090;

  width: 300px;
  background: var(--color-white, #fff);
  border-radius: 16px;
  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.14),
    0 4px 16px rgba(0, 0, 0, 0.08),
    0 0 0 1px rgba(0, 0, 0, 0.04);

  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* ── TRANSIÇÃO ───────────────────────────────────────────────── */
.painel-enter-active {
  transition: opacity 260ms ease, transform 280ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
.painel-leave-active {
  transition: opacity 180ms ease, transform 180ms ease;
}
.painel-enter-from,
.painel-leave-to {
  opacity: 0;
  transform: translateY(10px) scale(0.97);
  transform-origin: bottom right;
}

/* ── CABEÇALHO ───────────────────────────────────────────────── */
.a11y-painel__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  background: var(--color-primary-default, #1351B4);
  color: var(--color-white, #fff);
  flex-shrink: 0;
}

.a11y-painel__header-titulo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.03em;
}

.a11y-painel__header-icone {
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.a11y-painel__header-icone svg {
  width: 18px;
  height: 18px;
}

.a11y-painel__fechar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 150ms ease;
  flex-shrink: 0;
  padding: 0;
}
.a11y-painel__fechar svg {
  width: 12px;
  height: 12px;
  pointer-events: none;
}
.a11y-painel__fechar:hover      { background: rgba(255, 255, 255, 0.3); }
.a11y-painel__fechar:focus-visible {
  outline: 2px solid var(--color-warning, #FFCD07);
  outline-offset: 2px;
}

/* ── SEÇÕES ──────────────────────────────────────────────────── */
.a11y-painel__secao {
  padding: 14px 16px;
  border-bottom: 1px solid var(--color-gray-10, #E8E8E8);
}

.a11y-painel__secao-titulo {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-text-secondary, #555555);
  margin: 0 0 10px;
}

/* ── BOTÕES DE TEMA ──────────────────────────────────────────── */
.a11y-painel__tema-opcoes {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.a11y-painel__tema-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 10px 8px;
  border-radius: 10px;
  border: 2px solid var(--color-gray-10, #E8E8E8);
  background: var(--color-gray-05, #F8F8F8);
  cursor: pointer;
  transition: border-color 150ms ease, background 150ms ease;
  min-height: 62px;
}

.a11y-painel__tema-btn:hover {
  border-color: var(--color-primary-light, #2670E8);
  background: var(--color-primary-lightest, #DBE8FB);
}

.a11y-painel__tema-btn--ativo {
  border-color: var(--color-primary-default, #1351B4);
  background: var(--color-primary-lightest, #DBE8FB);
}

.a11y-painel__tema-btn:focus-visible {
  outline: 3px solid var(--color-border-focus, #C44601);
  outline-offset: 2px;
}

.a11y-painel__tema-icone { font-size: 22px; line-height: 1; }
.a11y-painel__tema-texto {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-primary, #1B1B1B);
}

/* ── TOGGLES GENÉRICOS ───────────────────────────────────────── */
.a11y-painel__toggle {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 10px;
  border-radius: 10px;
  border: 2px solid var(--color-gray-10, #E8E8E8);
  background: var(--color-gray-05, #F8F8F8);
  cursor: pointer;
  transition: border-color 150ms ease, background 150ms ease;
  text-align: left;
  min-height: 52px;
}

.a11y-painel__toggle:hover {
  border-color: var(--color-primary-light, #2670E8);
  background: var(--color-primary-lightest, #DBE8FB);
}

.a11y-painel__toggle--ativo {
  border-color: var(--color-primary-default, #1351B4);
  background: var(--color-primary-lightest, #DBE8FB);
}

.a11y-painel__toggle:focus-visible {
  outline: 3px solid var(--color-border-focus, #C44601);
  outline-offset: 2px;
}

/* Ícone do toggle */
.a11y-painel__toggle-icone {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: var(--color-primary-default, #1351B4);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: background 150ms ease;
}
.a11y-painel__toggle-icone svg { width: 18px; height: 18px; }
.a11y-painel__toggle-icone--emoji { font-size: 17px; }
.a11y-painel__toggle--ativo .a11y-painel__toggle-icone {
  background: var(--color-primary-dark, #0C326F);
}

/* Corpo do toggle */
.a11y-painel__toggle-corpo { flex: 1; min-width: 0; }
.a11y-painel__toggle-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-primary, #1B1B1B);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.a11y-painel__toggle-desc {
  display: block;
  font-size: 11px;
  color: var(--color-text-secondary, #555555);
  margin-top: 1px;
}

/* Pílula ON/OFF */
.a11y-painel__toggle-pill {
  flex-shrink: 0;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.06em;
  padding: 3px 7px;
  border-radius: 999px;
  background: var(--color-gray-20, #CCCCCC);
  color: var(--color-text-secondary, #555555);
  transition: background 150ms ease, color 150ms ease;
}

.a11y-painel__toggle--ativo .a11y-painel__toggle-pill {
  background: var(--color-primary-default, #1351B4);
  color: #fff;
}

.a11y-painel__toggle-pill--loading {
  background: var(--color-warning, #FFCD07);
  color: var(--color-primary-darker, #071D41);
}

/* ── CONTROLE DE FONTE ───────────────────────────────────────── */
.a11y-painel__fonte-controle {
  display: flex;
  align-items: center;
  gap: 10px;
}

.a11y-painel__fonte-btn {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  border: 2px solid var(--color-gray-20, #CCCCCC);
  background: var(--color-white, #fff);
  color: var(--color-primary-default, #1351B4);
  cursor: pointer;
  font-weight: 700;
  font-size: 14px;
  font-family: inherit;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: border-color 150ms ease, background 150ms ease;
  flex-shrink: 0;
  padding: 0;
}

.a11y-painel__fonte-btn:hover:not(:disabled) {
  border-color: var(--color-primary-default, #1351B4);
  background: var(--color-primary-lightest, #DBE8FB);
}

.a11y-painel__fonte-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.a11y-painel__fonte-btn:focus-visible {
  outline: 3px solid var(--color-border-focus, #C44601);
  outline-offset: 2px;
}

/* Dots indicadores de nível */
.a11y-painel__fonte-dots {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.a11y-painel__fonte-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--color-gray-20, #CCCCCC);
  transition: background 150ms ease, transform 150ms ease;
}

.a11y-painel__fonte-dot--ativo {
  background: var(--color-primary-default, #1351B4);
  transform: scale(1.35);
}

.a11y-painel__fonte-label {
  font-size: 11px;
  color: var(--color-text-secondary, #555555);
  text-align: center;
  margin: 8px 0 0;
}

/* ── RODAPÉ / RESETAR ────────────────────────────────────────── */
.a11y-painel__rodape {
  padding: 10px 16px;
  background: var(--color-gray-05, #F8F8F8);
  border-top: 1px solid var(--color-gray-10, #E8E8E8);
}

.a11y-painel__resetar {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: var(--color-text-secondary, #555555);
  font-size: 12px;
  font-family: inherit;
  font-weight: 600;
  cursor: pointer;
  transition: background 150ms ease, color 150ms ease;
}

.a11y-painel__resetar:hover {
  background: var(--color-danger-light, #FDE0DC);
  color: var(--color-accessible-red, #E52207);
}

.a11y-painel__resetar:focus-visible {
  outline: 3px solid var(--color-border-focus, #C44601);
  outline-offset: -1px;
  border-radius: 8px;
}

/* ── RESPONSIVO ──────────────────────────────────────────────── */
@media (max-width: 420px) {
  .a11y-painel {
    right: 12px;
    width: calc(100vw - 24px);
    max-width: 300px;
    bottom: 84px;
  }
}

/* ── REDUCED MOTION ──────────────────────────────────────────── */
@media (prefers-reduced-motion: reduce) {
  .painel-enter-active,
  .painel-leave-active { transition: opacity 100ms ease; }
  .painel-enter-from,
  .painel-leave-to     { transform: none; }
}
</style>