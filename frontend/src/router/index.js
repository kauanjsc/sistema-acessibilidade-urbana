/**
 * router/index.js
 * Configuração das rotas com proteção por autenticação.
 */

import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import { isAuthenticated } from '@/services/authService.js'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
      title: 'Início — Teresina Acessível',
      description: 'Plataforma de mapeamento de acessibilidade urbana em Teresina, PI.'
    }
  },
  {
    path: '/mapa',
    name: 'mapa',
    component: () => import('@/views/MapaView.vue'),
    meta: {
      title: 'Mapa Interativo — Teresina Acessível',
      description: 'Explore o mapa de acessibilidade da cidade de Teresina.'
    }
  },
  {
    path: '/contribuir',
    name: 'contribuir',
    component: () => import('@/views/ContribuirView.vue'),
    meta: {
      title: 'Contribuição Cidadã — Teresina Acessível',
      description: 'Avalie a acessibilidade de locais em Teresina.',
      requiresAuth: true   // 🔒 rota protegida
    }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue'),
    meta: {
      title: 'Entrar — Teresina Acessível',
      description: 'Acesse a plataforma Teresina Acessível.',
      guestOnly: true      // redireciona para /contribuir se já logado
    }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0, behavior: 'smooth' }
  }
})

// ── Navigation Guard global ───────────────────────────────────
router.beforeEach((to, from) => {
  const logado = isAuthenticated()

  // Rota protegida: usuário não autenticado → vai para /login
  if (to.meta.requiresAuth && !logado) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  // Página de login: usuário já autenticado → vai para /contribuir
  if (to.meta.guestOnly && logado) {
    return { name: 'contribuir' }
  }
})

// ── Atualiza <title> e meta description ──────────────────────
router.afterEach((to) => {
  document.title = to.meta?.title ?? 'Teresina Acessível'
  const metaDesc = document.querySelector('meta[name="description"]')
  if (metaDesc && to.meta?.description) {
    metaDesc.setAttribute('content', to.meta.description)
  }
})

export default router