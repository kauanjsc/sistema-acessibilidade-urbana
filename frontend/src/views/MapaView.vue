<template>
  <div class="mapa-view">

    <!-- Cabeçalho da view -->
    <div class="mapa-view__topbar">
      <div class="container mapa-view__topbar-inner">
        <div>
          <!--
            Heading da página — nível 1 pois é o título principal desta view.
            O <title> do documento já foi atualizado pelo router (WCAG 2.4.2).
          -->
          <h1 class="mapa-view__titulo">Mapa Interativo</h1>
          <p class="mapa-view__subtitulo">
            Explore a acessibilidade urbana de Teresina, PI
          </p>
        </div>

        <!-- Busca no topo do mapa -->
        <div class="mapa-view__busca">
          <BuscaLocal
            label="Buscar local"
            placeholder="Nome, bairro ou tipo de local..."
            :label-oculto="true"
            @select="selecionarLocal"
            @search="onBusca"
          />
        </div>
      </div>
    </div>

    <!-- Estado de carregamento -->
    <div v-if="carregando" class="mapa-view__loading" role="status" aria-live="polite">
      <span aria-hidden="true">⟳</span> Carregando locais...
    </div>
    <div v-if="erroCarregamento" class="mapa-view__erro" role="alert">
      {{ erroCarregamento }}
    </div>

    <!-- Área principal: filtros + mapa + painel -->
    <div v-if="!carregando" class="mapa-view__layout">

      <!-- Coluna 1: Filtros ─────────────────────────────── -->
      <!--
        <aside> com aria-label diferencia esta seção do conteúdo principal.
        É uma landmark region navegável via leitores de tela (WCAG 2.4.1).
      -->
      <aside
        class="mapa-view__filtros"
        :class="{ 'is-open': filtrosVisiveis }"
        aria-label="Painel de filtros"
      >
        <!-- Toggle para mobile -->
        <button
          class="mapa-view__filtros-toggle br-button secondary"
          type="button"
          :aria-expanded="filtrosVisiveis"
          aria-controls="filtros-panel"
          @click="filtrosVisiveis = !filtrosVisiveis"
        >
          <span aria-hidden="true">🔎</span>
          Filtros
          <span v-if="totalFiltrosAtivos > 0" class="filtros-badge" aria-label="filtros ativos">
            {{ totalFiltrosAtivos }}
          </span>
        </button>

        <div id="filtros-panel">
          <FiltroAcessibilidade @change="onFiltrosChange" />
        </div>
      </aside>

      <!-- Coluna 2: Mapa ───────────────────────────────── -->
      <div class="mapa-view__mapa">
        <MapaInterativo
          :locais="locaisFiltrados"
          :total-locais="todosLocais.length"
          :local-selecionado="localSelecionado"
          @selecionar="selecionarLocal"
        />
      </div>

      <!-- Coluna 3: Painel de detalhes ────────────────── -->
      <PainelDetalhes
        :local="localSelecionado"
        @fechar="localSelecionado = null"
      />

    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import BuscaLocal from '@/components/BuscaLocal.vue'
import FiltroAcessibilidade from '@/components/FiltroAcessibilidade.vue'
import MapaInterativo from '@/components/MapaInterativo.vue'
import PainelDetalhes from '@/components/PainelDetalhes.vue'
import {
  getLocais,
  filtrarPorBusca,
  filtrarPorAcessibilidade,
  filtrarPorNivel,
  getLocalById
} from '@/services/acessibilidadeService.js'

const route = useRoute()

// ── Estado ────────────────────────────────────────────────────
const todosLocais      = ref([])
const carregando       = ref(true)
const erroCarregamento = ref(null)
const localSelecionado = ref(null)
const filtrosVisiveis  = ref(true)

// Estado dos filtros
const busca = ref('')
const filtrosRecursos = ref({})
const filtrosNiveis = ref([])
const totalFiltrosAtivos = ref(0)

// ── Locais filtrados (computed reativo) ───────────────────────
const locaisFiltrados = computed(() => {
  let lista = todosLocais.value

  if (busca.value) {
    lista = filtrarPorBusca(lista, busca.value)
  }
  if (Object.keys(filtrosRecursos.value).length > 0) {
    lista = filtrarPorAcessibilidade(lista, filtrosRecursos.value)
  }
  if (filtrosNiveis.value.length > 0) {
    lista = filtrarPorNivel(lista, filtrosNiveis.value)
  }

  return lista
})

// ── Handlers ─────────────────────────────────────────────────
function selecionarLocal(local) {
  localSelecionado.value = local
}

function onBusca(query) {
  busca.value = query
}

function onFiltrosChange({ recursos, niveis }) {
  filtrosRecursos.value = recursos
  filtrosNiveis.value = niveis
  totalFiltrosAtivos.value =
    Object.keys(recursos).length + niveis.length
}

// ── Carrega locais e trata query params ───────────────────────
onMounted(async () => {
  try {
    carregando.value = true
    todosLocais.value = await getLocais()

    // Abre local diretamente por URL (?id=4)
    if (route.query.id) {
      const local = todosLocais.value.find(l => l.id === Number(route.query.id))
      if (local) selecionarLocal(local)
    }
    if (route.query.busca) {
      busca.value = String(route.query.busca)
    }
  } catch (err) {
    erroCarregamento.value = 'Não foi possível carregar os locais. Tente novamente.'
    console.error('[MapaView] erro ao carregar locais:', err)
  } finally {
    carregando.value = false
  }
})
</script>

<style scoped>
.mapa-view {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 88px); /* 88px = govbr-bar + header */
}

/* Topbar */
.mapa-view__topbar {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-gray-10);
  padding: var(--space-4) 0;
  flex-shrink: 0;
}
.mapa-view__topbar-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-6);
}
.mapa-view__titulo {
  font-size: var(--font-size-xl);
  color: var(--color-primary-dark);
  margin-bottom: 0;
}
.mapa-view__subtitulo {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-bottom: 0;
}
.mapa-view__busca {
  flex: 1;
  max-width: 400px;
}

/* Layout principal */
.mapa-view__layout {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* Filtros */
.mapa-view__filtros {
  width: 280px;
  min-width: 280px;
  overflow-y: auto;
  background: var(--color-surface);
  border-right: 1px solid var(--color-gray-10);
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.mapa-view__filtros-toggle { display: none; }
.filtros-badge {
  background: var(--color-primary-default);
  color: white;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  padding: 1px var(--space-2);
  font-weight: 700;
}

/* Mapa */
.mapa-view__mapa {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* ── RESPONSIVO ─────────────────────────────────────────── */
@media (max-width: 1100px) {
  .mapa-view__topbar-inner { flex-direction: column; align-items: flex-start; }
  .mapa-view__busca { max-width: 100%; width: 100%; }
}

@media (max-width: 900px) {
  .mapa-view {
    height: auto;
    min-height: calc(100vh - 88px);
  }
  .mapa-view__layout {
    flex-direction: column;
    overflow: visible;
  }
  .mapa-view__filtros {
    width: 100%;
    min-width: unset;
    border-right: none;
    border-bottom: 1px solid var(--color-gray-10);
    overflow: visible;
  }
  .mapa-view__filtros-toggle {
    display: flex;
    align-self: flex-start;
  }
  #filtros-panel {
    display: none;
  }
  .mapa-view__filtros.is-open #filtros-panel {
    display: block;
    padding-top: var(--space-3);
  }
  .mapa-view__mapa {
    min-height: 400px;
  }
}

.mapa-view__loading {
  padding: var(--space-8);
  text-align: center;
  color: var(--color-text-secondary);
  font-size: var(--font-size-md);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
}
.mapa-view__loading span {
  display: inline-block;
  animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.mapa-view__erro {
  margin: var(--space-4);
  padding: var(--space-4);
  background: var(--color-danger-light);
  color: var(--color-accessible-red);
  border-left: 4px solid var(--color-accessible-red);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
}
</style>