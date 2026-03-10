<template>
  <!--
    role="application" não é usado aqui pois reduziria recursos nativos
    do browser. A estrutura semântica com <header>, <main> e <footer>
    é suficiente para WCAG 1.3.1 (Info and Relationships).
  -->
  <div id="app-root">
    <AppHeader />

    <!--
      aria-live="polite": anuncia mudanças de rota para leitores de tela
      sem interromper o que está sendo lido (WCAG 4.1.3).
    -->
    <div
      aria-live="polite"
      aria-atomic="true"
      class="sr-only"
      role="status"
    >
      {{ routeAnnouncement }}
    </div>

    <main id="main-content" tabindex="-1">
      <!--
        RouterView com transição suave.
        mode="out-in" garante que a página anterior saia antes
        da nova entrar, evitando confusão em leitores de tela.
      -->
      <RouterView v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" :key="$route.path" />
        </Transition>
      </RouterView>
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'

const route = useRoute()
const routeAnnouncement = ref('')

/**
 * Anuncia a navegação para leitores de tela.
 * Quando o título da página muda, informa o usuário (WCAG 2.4.2).
 */
watch(
  () => route.meta?.title,
  (newTitle) => {
    if (newTitle) {
      routeAnnouncement.value = `Navegou para: ${newTitle}`
      // Limpa após anúncio para permitir repetição
      setTimeout(() => { routeAnnouncement.value = '' }, 1000)
    }
  }
)
</script>

<style>
/* Transição de página — respeita prefers-reduced-motion */
.page-enter-active,
.page-leave-active {
  transition: opacity 200ms ease, transform 200ms ease;
}
.page-enter-from {
  opacity: 0;
  transform: translateY(8px);
}
.page-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

#app-root {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

#main-content {
  flex: 1;
  /* outline none pois o foco aqui é programático (skip link) */
  outline: none;
}
</style>
