<template>
  <div id="app-root">
    <AppHeader />

    <!-- Anuncia mudanças de rota para leitores de tela (WCAG 4.1.3) -->
    <div
      aria-live="polite"
      aria-atomic="true"
      class="sr-only"
      role="status"
    >
      {{ routeAnnouncement }}
    </div>

    <main id="main-content" tabindex="-1">
      <RouterView v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" :key="$route.path" />
        </Transition>
      </RouterView>
    </main>

    <AppFooter />

    <!--
      Barra de Acessibilidade — dividida em dois componentes:
        AccessibilityButton → botão fixo no canto inferior direito
        AccessibilityPanel  → painel flutuante acima do botão
      Ambos compartilham estado via useAcessibilidade() (composable singleton).
    -->
    <AccessibilityPanel />
    <AccessibilityButton />
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
import AccessibilityButton from '@/components/acessibilidade/AccessibilityButton.vue'
import AccessibilityPanel  from '@/components/acessibilidade/AccessibilityPanel.vue'
import { useAcessibilidade } from '@/services/useAcessibilidade.js'

const route = useRoute()
const routeAnnouncement = ref('')

// Anuncia navegação para leitores de tela
watch(
  () => route.meta?.title,
  (newTitle) => {
    if (newTitle) {
      routeAnnouncement.value = `Navegou para: ${newTitle}`
      setTimeout(() => { routeAnnouncement.value = '' }, 1000)
    }
  }
)

// Fecha o painel de acessibilidade com ESC (WCAG 2.1.2)
const { fecharPainel, restaurarPreferencias } = useAcessibilidade()

function onKeydown(e) {
  if (e.key === 'Escape') fecharPainel()
}

onMounted(() => {
  // Restaura preferências salvas no localStorage
  restaurarPreferencias()
  document.addEventListener('keydown', onKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', onKeydown)
})
</script>

<style>
/* Transição de página — respeita prefers-reduced-motion */
.page-enter-active,
.page-leave-active {
  transition: opacity 200ms ease, transform 200ms ease;
}
.page-enter-from { opacity: 0; transform: translateY(8px); }
.page-leave-to   { opacity: 0; transform: translateY(-8px); }

@media (prefers-reduced-motion: reduce) {
  .page-enter-active,
  .page-leave-active { transition: opacity 100ms ease; }
  .page-enter-from,
  .page-leave-to     { transform: none; }
}

#app-root {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

#main-content {
  flex: 1;
  outline: none;
}
</style>