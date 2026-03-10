<template>
  <header class="app-header" role="banner">

    <!-- Barra gov.br -->
    <div class="govbr-bar" role="complementary" aria-label="Barra do Governo Federal">
      <div class="container govbr-bar__inner">
        <span class="govbr-bar__logo" aria-hidden="true">
          <svg width="48" height="20" viewBox="0 0 120 40" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">
            <rect width="120" height="40" fill="#1351B4"/>
            <text x="8" y="28" fill="white" font-size="20" font-family="Rawline,sans-serif" font-weight="700">gov.br</text>
          </svg>
        </span>
        <span class="govbr-bar__text">Governo Federal — Brasil</span>
      </div>
    </div>

    <!-- Cabeçalho principal -->
    <div class="app-header__main">
      <div class="container app-header__inner">

        <!-- Logo -->
        <RouterLink to="/" class="app-header__brand" :aria-label="`Teresina Acessível — ir para a página inicial`">
          <span class="app-header__brand-icon" aria-hidden="true">♿</span>
          <span class="app-header__brand-text">
            <span class="app-header__brand-name">Teresina</span>
            <span class="app-header__brand-tagline">Acessível</span>
          </span>
        </RouterLink>

        <!-- Navegação principal desktop -->
        <nav aria-label="Navegação principal" class="app-header__nav">
          <ul role="list" class="app-header__nav-list">
            <li>
              <RouterLink to="/" class="app-header__nav-link" :aria-current="$route.name === 'home' ? 'page' : undefined">
                Início
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/mapa" class="app-header__nav-link" :aria-current="$route.name === 'mapa' ? 'page' : undefined">
                Mapa Interativo
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/contribuir" class="app-header__nav-link app-header__nav-link--destaque" :aria-current="$route.name === 'contribuir' ? 'page' : undefined">
                ✍️ Contribuir
              </RouterLink>
            </li>
          </ul>
        </nav>

        <!-- Área do usuário (desktop) -->
        <div class="app-header__usuario" aria-label="Conta do usuário">

          <!-- Logado: avatar + nome + logout -->
          <div v-if="autenticado" class="app-header__user-info">
            <div class="app-header__avatar" aria-hidden="true">
              {{ usuarioAtual.avatar }}
            </div>
            <span class="app-header__user-nome" :title="usuarioAtual.email">
              {{ nomeAbreviado }}
            </span>
            <button
              type="button"
              class="app-header__btn-logout br-button tertiary"
              aria-label="Sair da conta"
              title="Sair"
              @click="fazerLogout"
            >
              <span aria-hidden="true">🚪</span>
              <span class="app-header__btn-logout-texto">Sair</span>
            </button>
          </div>

          <!-- Deslogado: botão entrar -->
          <RouterLink
            v-else
            to="/login"
            class="app-header__btn-login"
            aria-label="Entrar na plataforma"
          >
            🔓 Entrar
          </RouterLink>

        </div>

        <!-- Toggle mobile -->
        <button
          class="app-header__menu-toggle br-button tertiary"
          :aria-expanded="mobileMenuOpen"
          aria-controls="mobile-menu"
          aria-label="Abrir menu de navegação"
          @click="toggleMobileMenu"
        >
          <span aria-hidden="true">{{ mobileMenuOpen ? '✕' : '☰' }}</span>
        </button>

      </div>
    </div>

    <!-- Menu mobile -->
    <div
      v-if="mobileMenuOpen"
      id="mobile-menu"
      class="app-header__mobile-menu"
      role="dialog"
      aria-label="Menu de navegação"
      aria-modal="false"
    >
      <nav aria-label="Navegação mobile">
        <ul role="list">
          <li>
            <RouterLink to="/" class="app-header__mobile-link" :aria-current="$route.name === 'home' ? 'page' : undefined" @click="closeMobileMenu">
              🏠 Início
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/mapa" class="app-header__mobile-link" :aria-current="$route.name === 'mapa' ? 'page' : undefined" @click="closeMobileMenu">
              🗺️ Mapa Interativo
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/contribuir" class="app-header__mobile-link app-header__mobile-link--destaque" :aria-current="$route.name === 'contribuir' ? 'page' : undefined" @click="closeMobileMenu">
              ✍️ Contribuir
            </RouterLink>
          </li>
        </ul>
      </nav>

      <!-- Info do usuário no mobile -->
      <div class="app-header__mobile-user">
        <div v-if="autenticado" class="app-header__mobile-user-info">
          <div class="app-header__avatar" aria-hidden="true">{{ usuarioAtual.avatar }}</div>
          <div>
            <p class="app-header__mobile-user-nome">{{ usuarioAtual.nome }}</p>
            <p class="app-header__mobile-user-email">{{ usuarioAtual.email }}</p>
          </div>
          <button type="button" class="br-button secondary app-header__mobile-logout" @click="fazerLogout">
            🚪 Sair
          </button>
        </div>
        <RouterLink v-else to="/login" class="br-button primary app-header__mobile-login" @click="closeMobileMenu">
          🔓 Entrar na plataforma
        </RouterLink>
      </div>
    </div>

  </header>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/services/authService.js'

const route  = useRoute()
const router = useRouter()
const { usuarioAtual, autenticado, logout } = useAuth()

const mobileMenuOpen = ref(false)

function toggleMobileMenu() { mobileMenuOpen.value = !mobileMenuOpen.value }
function closeMobileMenu()  { mobileMenuOpen.value = false }

watch(() => route.path, closeMobileMenu)

// Exibe só o primeiro nome no desktop para economizar espaço
const nomeAbreviado = computed(() => {
  if (!usuarioAtual.value) return ''
  return usuarioAtual.value.nome.split(' ')[0]
})

function fazerLogout() {
  logout()
  closeMobileMenu()
  router.push('/')
}
</script>

<style scoped>
/* ── BARRA GOVBR ────────────────────────────────────────────── */
.govbr-bar {
  background: var(--color-primary-darker);
  color: var(--color-white);
  padding: var(--space-1) 0;
  font-size: var(--font-size-xs);
}
.govbr-bar__inner { display: flex; align-items: center; gap: var(--space-2); }
.govbr-bar__text  { font-size: var(--font-size-xs); font-weight: var(--font-weight-medium); color: rgba(255,255,255,.85); }

/* ── CABEÇALHO PRINCIPAL ────────────────────────────────────── */
.app-header__main {
  background: var(--color-primary-default);
  box-shadow: 0 2px 8px rgba(0,0,0,.2);
  position: sticky; top: 0; z-index: 100;
}
.app-header__inner {
  display: flex; align-items: center;
  justify-content: space-between; height: 64px; gap: var(--space-4);
}

/* ── MARCA ──────────────────────────────────────────────────── */
.app-header__brand {
  display: flex; align-items: center; gap: var(--space-3);
  text-decoration: none; color: var(--color-white); flex-shrink: 0;
}
.app-header__brand:hover { opacity: 0.9; }
.app-header__brand-icon  { font-size: 1.75rem; line-height: 1; }
.app-header__brand-text  { display: flex; flex-direction: column; line-height: 1.1; }
.app-header__brand-name  { font-size: var(--font-size-lg); font-weight: var(--font-weight-extrabold); letter-spacing: -0.01em; }
.app-header__brand-tagline { font-size: var(--font-size-xs); font-weight: var(--font-weight-medium); opacity: .85; letter-spacing: .08em; text-transform: uppercase; }

/* ── NAVEGAÇÃO ──────────────────────────────────────────────── */
.app-header__nav { display: block; }
.app-header__nav-list { display: flex; list-style: none; gap: var(--space-2); }
.app-header__nav-link {
  display: block; padding: var(--space-2) var(--space-4);
  color: var(--color-white); text-decoration: none;
  font-weight: var(--font-weight-semibold); font-size: var(--font-size-sm);
  border-radius: var(--radius-full); border: 2px solid transparent;
  transition: background var(--transition-fast), border-color var(--transition-fast);
  white-space: nowrap;
}
.app-header__nav-link:hover { background: rgba(255,255,255,.15); }
.app-header__nav-link[aria-current="page"] { background: rgba(255,255,255,.2); border-color: rgba(255,255,255,.6); }
.app-header__nav-link--destaque {
  background: var(--color-warning); color: var(--color-primary-darker) !important;
  border-color: var(--color-warning); font-weight: var(--font-weight-bold) !important;
}
.app-header__nav-link--destaque:hover { background: #e6b800; border-color: #e6b800; }

/* ── ÁREA DO USUÁRIO ─────────────────────────────────────────── */
.app-header__usuario { display: flex; align-items: center; flex-shrink: 0; }

.app-header__user-info {
  display: flex; align-items: center; gap: var(--space-3);
  background: rgba(255,255,255,.1);
  border: 1px solid rgba(255,255,255,.2);
  border-radius: var(--radius-full);
  padding: var(--space-1) var(--space-2) var(--space-1) var(--space-1);
}
.app-header__avatar {
  width: 32px; height: 32px;
  background: var(--color-warning);
  color: var(--color-primary-darker);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: var(--font-size-xs); font-weight: var(--font-weight-bold);
  flex-shrink: 0;
}
.app-header__user-nome {
  font-size: var(--font-size-sm); font-weight: var(--font-weight-semibold);
  color: var(--color-white); max-width: 120px;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.app-header__btn-logout {
  color: rgba(255,255,255,.8) !important;
  padding: var(--space-1) var(--space-2) !important;
  min-height: unset !important;
  display: flex; align-items: center; gap: 4px;
  font-size: var(--font-size-xs) !important;
}
.app-header__btn-logout:hover { color: var(--color-white) !important; }

.app-header__btn-login {
  display: flex; align-items: center; gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: rgba(255,255,255,.15);
  color: var(--color-white);
  border: 1px solid rgba(255,255,255,.4);
  border-radius: var(--radius-full);
  text-decoration: none;
  font-size: var(--font-size-sm); font-weight: var(--font-weight-semibold);
  transition: background var(--transition-fast);
  white-space: nowrap;
}
.app-header__btn-login:hover { background: rgba(255,255,255,.25); }

/* ── MENU TOGGLE (mobile) ───────────────────────────────────── */
.app-header__menu-toggle {
  display: none; color: var(--color-white) !important; font-size: var(--font-size-xl);
}

/* ── MENU MOBILE ────────────────────────────────────────────── */
.app-header__mobile-menu { background: var(--color-primary-dark); padding: var(--space-4); }
.app-header__mobile-menu ul { list-style: none; display: flex; flex-direction: column; gap: var(--space-2); }
.app-header__mobile-link {
  display: block; padding: var(--space-3) var(--space-4);
  color: var(--color-white); text-decoration: none;
  font-weight: var(--font-weight-semibold);
  border-radius: var(--radius-md); transition: background var(--transition-fast);
}
.app-header__mobile-link:hover,
.app-header__mobile-link[aria-current="page"] { background: rgba(255,255,255,.15); }
.app-header__mobile-link--destaque {
  background: var(--color-warning); color: var(--color-primary-darker) !important;
  font-weight: var(--font-weight-bold) !important;
}
.app-header__mobile-link--destaque:hover { background: #e6b800; }

.app-header__mobile-user {
  margin-top: var(--space-4); padding-top: var(--space-4);
  border-top: 1px solid rgba(255,255,255,.15);
}
.app-header__mobile-user-info {
  display: flex; align-items: center; gap: var(--space-3); flex-wrap: wrap;
}
.app-header__mobile-user-nome { font-weight: var(--font-weight-bold); color: var(--color-white); font-size: var(--font-size-sm); margin-bottom: 2px; }
.app-header__mobile-user-email { font-size: var(--font-size-xs); color: rgba(255,255,255,.7); margin-bottom: 0; }
.app-header__mobile-logout { font-size: var(--font-size-sm) !important; margin-left: auto; }
.app-header__mobile-login  { display: block; text-align: center; text-decoration: none; width: 100%; justify-content: center; }

/* ── RESPONSIVO ─────────────────────────────────────────────── */
@media (max-width: 900px) {
  .app-header__nav     { display: none; }
  .app-header__usuario { display: none; }
  .app-header__menu-toggle { display: inline-flex; }
}
@media (max-width: 400px) {
  .app-header__btn-logout-texto { display: none; }
}
</style>