/**
 * useAcessibilidade.js
 * Composable singleton que centraliza o estado e as ações de
 * acessibilidade, compartilhado entre AccessibilityButton e
 * AccessibilityPanel sem prop drilling.
 *
 * Localização: src/components/acessibilidade/useAcessibilidade.js
 */

import { ref, computed } from 'vue'

// ── Constantes ────────────────────────────────────────────────
const FONTE_BASE  = 16
const FONTE_MIN   = 14
const FONTE_MAX   = 22
const PASSO_FONTE = 2
const STORAGE_KEY = 'ta_acessibilidade'

// ── Estado reativo (module-level = singleton entre componentes) ──
const painelAberto     = ref(false)
const modoEscuro       = ref(false)
const altoContraste    = ref(false)
const tamanhoFonte     = ref(FONTE_BASE)
const navegacaoTeclado = ref(false)
const vlibrasAtivo     = ref(false)
const vlibrasCarregando = ref(false)

// ── Computed: total de recursos ativos (usado no badge) ───────
const totalAtivos = computed(() => [
  modoEscuro.value,
  altoContraste.value,
  tamanhoFonte.value !== FONTE_BASE,
  navegacaoTeclado.value,
  vlibrasAtivo.value,
].filter(Boolean).length)

// ─────────────────────────────────────────────────────────────
// AÇÕES
// ─────────────────────────────────────────────────────────────

function abrirPainel()  { painelAberto.value = true  }
function fecharPainel() { painelAberto.value = false }
function togglePainel() { painelAberto.value = !painelAberto.value }

// Modo escuro
function setModoEscuro(ativo) {
  modoEscuro.value = ativo
  document.body.classList.toggle('modo-escuro', ativo)
  salvar()
}

// Alto contraste
function toggleAltoContraste() {
  altoContraste.value = !altoContraste.value
  document.body.classList.toggle('alto-contraste', altoContraste.value)
  salvar()
}

// Tamanho de fonte
function ajustarFonte(delta) {
  tamanhoFonte.value = Math.min(
    FONTE_MAX,
    Math.max(FONTE_MIN, tamanhoFonte.value + delta * PASSO_FONTE)
  )
  document.documentElement.style.fontSize = tamanhoFonte.value + 'px'
  salvar()
}

// Navegação por teclado
function toggleNavTeclado() {
  navegacaoTeclado.value = !navegacaoTeclado.value
  document.body.classList.toggle('foco-aprimorado', navegacaoTeclado.value)
  salvar()
}

// VLibras
function toggleVLibras() {
  vlibrasAtivo.value ? _desativarVLibras() : _ativarVLibras()
}

function _ativarVLibras() {
  vlibrasAtivo.value      = true
  vlibrasCarregando.value = true

  // 1. Injeta o container HTML obrigatório que o VLibras precisa no DOM
  if (!document.getElementById('vlibras-container')) {
    const container = document.createElement('div')
    container.id = 'vlibras-container'
    container.setAttribute('vw', '')
    container.className = 'enabled'
    container.innerHTML = `
      <div vw-access-button class="active"></div>
      <div vw-plugin-wrapper>
        <div class="vw-plugin-top-wrapper"></div>
      </div>
    `
    document.body.appendChild(container)
  } else {
    // Container já existe — apenas mostra
    document.getElementById('vlibras-container').style.display = 'block'
  }

  // 2. Se o script já foi carregado antes, só re-inicializa
  if (window.VLibras) {
    _inicializarVLibras()
    return
  }

  // 3. Carrega o script do VLibras pela primeira vez
  const script = document.createElement('script')
  script.src     = 'https://vlibras.gov.br/app/vlibras-plugin.js'
  script.async   = true
  script.id      = 'vlibras-script'
  script.onload  = _inicializarVLibras
  script.onerror = () => {
    vlibrasCarregando.value = false
    vlibrasAtivo.value      = false
    console.warn('[VLibras] falha ao carregar o script. Verifique sua conexão.')
  }
  document.head.appendChild(script)
  salvar()
}

function _inicializarVLibras() {
  vlibrasCarregando.value = false
  try {
    new window.VLibras.Widget('https://vlibras.gov.br/app')
  } catch (e) {
    // Widget já inicializado — comportamento esperado ao reativar
  }
}

function _desativarVLibras() {
  vlibrasAtivo.value = false
  const container = document.getElementById('vlibras-container')
  if (container) container.style.display = 'none'
  salvar()
}

// Resetar todas as preferências
function resetarTudo() {
  setModoEscuro(false)
  if (altoContraste.value)    toggleAltoContraste()
  if (navegacaoTeclado.value) toggleNavTeclado()
  if (vlibrasAtivo.value)     _desativarVLibras()
  tamanhoFonte.value = FONTE_BASE
  document.documentElement.style.fontSize = ''
  localStorage.removeItem(STORAGE_KEY)
}

// ─────────────────────────────────────────────────────────────
// PERSISTÊNCIA
// ─────────────────────────────────────────────────────────────

function salvar() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      modoEscuro:       modoEscuro.value,
      altoContraste:    altoContraste.value,
      tamanhoFonte:     tamanhoFonte.value,
      navegacaoTeclado: navegacaoTeclado.value,
      vlibrasAtivo:     vlibrasAtivo.value,
    }))
  } catch { /* storage cheio ou bloqueado */ }
}

function restaurarPreferencias() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return
    const p = JSON.parse(raw)
    if (p.modoEscuro)       setModoEscuro(true)
    if (p.altoContraste)    toggleAltoContraste()
    if (p.tamanhoFonte && p.tamanhoFonte !== FONTE_BASE) {
      tamanhoFonte.value = p.tamanhoFonte
      document.documentElement.style.fontSize = p.tamanhoFonte + 'px'
    }
    if (p.navegacaoTeclado) toggleNavTeclado()
    if (p.vlibrasAtivo)     _ativarVLibras()
  } catch { /* JSON inválido */ }
}

// ─────────────────────────────────────────────────────────────
// COMPOSABLE EXPORT
// ─────────────────────────────────────────────────────────────

export function useAcessibilidade() {
  return {
    // Estado (readonly por convenção)
    painelAberto,
    modoEscuro,
    altoContraste,
    tamanhoFonte,
    navegacaoTeclado,
    vlibrasAtivo,
    vlibrasCarregando,
    totalAtivos,

    // Constantes
    FONTE_BASE,
    FONTE_MIN,
    FONTE_MAX,

    // Ações
    abrirPainel,
    fecharPainel,
    togglePainel,
    setModoEscuro,
    toggleAltoContraste,
    ajustarFonte,
    toggleNavTeclado,
    toggleVLibras,
    resetarTudo,
    restaurarPreferencias,
  }
}