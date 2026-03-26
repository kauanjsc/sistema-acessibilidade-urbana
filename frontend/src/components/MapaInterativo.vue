<template>
  <div class="mapa-wrapper">

    <!--
      O mapa Leaflet não é acessível por si só (canvas/SVG sem texto).
      Fornecemos uma alternativa textual via tabela (WCAG 1.1.1 e WCAG 4.1.2).
      O usuário pode alternar entre Mapa e Tabela via botões.
    -->
    <div class="mapa-controles" role="toolbar" aria-label="Controles de visualização do mapa">
      <button
        class="br-button"
        :class="visualizacao === 'mapa' ? 'primary' : 'secondary'"
        type="button"
        :aria-pressed="visualizacao === 'mapa'"
        @click="visualizacao = 'mapa'"
      >
        <MapIcon aria-hidden="true" :size="18" style="display: inline; vertical-align: text-bottom; margin-right: 4px;" /> Mapa
      </button>
      <button
        class="br-button"
        :class="visualizacao === 'tabela' ? 'primary' : 'secondary'"
        type="button"
        :aria-pressed="visualizacao === 'tabela'"
        @click="visualizacao = 'tabela'"
      >
        <Table aria-hidden="true" :size="18" style="display: inline; vertical-align: text-bottom; margin-right: 4px;" /> Tabela
      </button>
    </div>

    <!-- Contador de resultados -->
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
      class="mapa-contador"
    >
      Exibindo <strong>{{ locais.length }}</strong>
      local{{ locais.length !== 1 ? 'is' : '' }}
      <span v-if="locais.length !== totalLocais">
        de {{ totalLocais }} no total
      </span>
    </div>

    <!-- Visualização: MAPA ──────────────────────────────────── -->
    <div v-show="visualizacao === 'mapa'" class="mapa-container">
      <!--
        aria-label descreve o mapa para tecnologias assistivas.
        role="application" é adequado aqui pois o usuário interage
        com controles dentro do widget (WCAG 4.1.2).
        tabindex="0" permite foco via teclado.
      -->
      <div
        ref="mapEl"
        class="mapa-leaflet"
        role="application"
        aria-label="Mapa interativo de acessibilidade de Teresina. Use as setas para navegar. Pressione Tab para acessar os marcadores."
        tabindex="0"
      ></div>

      <!-- Legenda do mapa -->
      <div class="mapa-legenda" role="note" aria-label="Legenda das cores dos marcadores">
        <h3 class="mapa-legenda__titulo">Legenda</h3>
        <ul role="list" class="mapa-legenda__lista">
          <li class="mapa-legenda__item">
            <span class="mapa-legenda__dot dot-total" aria-hidden="true"></span>
            <span>Totalmente Acessível</span>
          </li>
          <li class="mapa-legenda__item">
            <span class="mapa-legenda__dot dot-parcial" aria-hidden="true"></span>
            <span>Parcialmente Acessível</span>
          </li>
          <li class="mapa-legenda__item">
            <span class="mapa-legenda__dot dot-nao" aria-hidden="true"></span>
            <span>Não Acessível</span>
          </li>
        </ul>
      </div>
    </div>

    <!-- Visualização: TABELA (alternativa acessível ao mapa) ── -->
    <div v-show="visualizacao === 'tabela'" class="mapa-tabela-wrapper">
      <!--
        caption descreve a tabela para leitores de tela (WCAG 1.3.1).
        scope="col" nas células de cabeçalho associa coluna ao dado.
      -->
      <table class="mapa-tabela" aria-label="Lista de locais com dados de acessibilidade">
        <caption class="sr-only">
          Tabela com {{ locais.length }} locais de Teresina e seus recursos de acessibilidade.
        </caption>
        <thead>
          <tr>
            <th scope="col">Local</th>
            <th scope="col">Tipo</th>
            <th scope="col">Bairro</th>
            <th scope="col">Nível</th>
            <th scope="col" v-for="(meta, chave) in RECURSOS_META" :key="chave">
              <abbr :title="meta.label">
                <component :is="mapaIconesTabela[meta.icone]" :size="18" aria-hidden="true" />
              </abbr>
            </th>
            <th scope="col"><span class="sr-only">Ação</span></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="local in locais"
            :key="local.id"
            class="mapa-tabela__row"
            :class="`row-${local.classificacao.nivel}`"
            @click="$emit('selecionar', local)"
            @keydown.enter="$emit('selecionar', local)"
            @keydown.space.prevent="$emit('selecionar', local)"
            tabindex="0"
            role="button"
            :aria-label="`Ver detalhes de ${local.nome}`"
          >
            <td class="mapa-tabela__nome">{{ local.nome }}</td>
            <td>{{ local.tipoLabel }}</td>
            <td>{{ local.bairro }}</td>
            <td>
              <BadgeAcessibilidade
                :nivel="local.classificacao.nivel"
                :label="local.classificacao.label"
              />
            </td>
            <td
              v-for="(meta, chave) in RECURSOS_META"
              :key="chave"
              class="mapa-tabela__recurso"
              :aria-label="`${meta.label}: ${local.acessibilidade[chave] ? 'disponível' : 'não disponível'}`"
            >
              <span :class="local.acessibilidade[chave] ? 'text-sim' : 'text-nao'" aria-hidden="true">
                <Check v-if="local.acessibilidade[chave]" :size="16" style="vertical-align: text-bottom;" />
                <X v-else :size="16" style="vertical-align: text-bottom;" />
              </span>
            </td>
            <td>
              <button
                class="br-button secondary mapa-tabela__btn"
                type="button"
                :aria-label="`Ver detalhes de acessibilidade de ${local.nome}`"
                @click.stop="$emit('selecionar', local)"
              >
                Detalhes
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import BadgeAcessibilidade from '@/components/BadgeAcessibilidade.vue'
import { RECURSOS_META } from '@/services/acessibilidadeService.js'
import { Accessibility, Users, CircleParking, ArrowUpCircle, DoorOpen, Footprints, Map as MapIcon, Table, Check, X } from 'lucide-vue-next'

// Dicionário para traduzir a string do service para o ícone
const mapaIconesTabela = {
  'Accessibility': Accessibility,
  'Users': Users,
  'ParkingCircle': CircleParking, 
  'ArrowUpCircle': ArrowUpCircle,
  'DoorOpen': DoorOpen,
  'Footprints': Footprints
}

const props = defineProps({
  locais: { type: Array, default: () => [] },
  totalLocais: { type: Number, default: 0 },
  localSelecionado: { type: Object, default: null }
})

const emit = defineEmits(['selecionar'])

const mapEl = ref(null)
const visualizacao = ref('mapa')

// Instâncias do Leaflet
let mapInstance = null
const markers = new Map()

// ── CORES DOS MARCADORES ─────────────────────────────────────
const CORES_NIVEL = {
  total:   '#168821',   // verde gov.br
  parcial: '#B87900',   // amarelo escuro
  nao:     '#E52207'    // vermelho gov.br
}

/**
 * Cria um ícone SVG customizado para o marcador Leaflet.
 * Usamos SVG inline para controle total de cor e acessibilidade.
 */
function criarIcone(nivel) {
  const cor = CORES_NIVEL[nivel]
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="40" viewBox="0 0 32 40">
      <path d="M16 0C7.163 0 0 7.163 0 16c0 10 16 24 16 24S32 26 32 16C32 7.163 24.837 0 16 0z"
            fill="${cor}" stroke="white" stroke-width="2"/>
      <text x="16" y="22" text-anchor="middle" font-size="14" fill="white">♿</text>
    </svg>
  `.trim()

  // Importação dinâmica do Leaflet
  const L = window.L
  return L.divIcon({
    html: svg,
    className: 'mapa-marcador',
    iconSize: [32, 40],
    iconAnchor: [16, 40],
    popupAnchor: [0, -40]
  })
}

/**
 * Gera o HTML do popup do marcador.
 * Popup simples e focável — o painel lateral tem a informação completa.
 */
function criarPopupHtml(local) {
  const { nivel, label } = local.classificacao
  const corTexto = nivel === 'total' ? '#168821' : nivel === 'parcial' ? '#B87900' : '#E52207'
  return `
    <div style="min-width:200px;font-family:'Rawline',sans-serif;">
      <p style="font-size:11px;font-weight:600;color:#555;text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px;">
        ${local.tipoLabel}
      </p>
      <strong style="font-size:15px;color:#071D41;display:block;margin-bottom:4px;">${local.nome}</strong>
      <p style="font-size:12px;color:#555;margin-bottom:8px;">${local.bairro}</p>
      <span style="font-size:12px;font-weight:700;color:${corTexto};">● ${label}</span>
    </div>
  `
}

async function inicializarMapa() {
  await nextTick()
  if (!mapEl.value) return

  // Importação dinâmica do Leaflet (evita SSR issues)
  const L = await import('leaflet')
  window.L = L.default ?? L

  // Corrige ícones padrão quebrados no Vite/Webpack
  delete window.L.Icon.Default.prototype._getIconUrl
  window.L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
    iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png'
  })

  mapInstance = window.L.map(mapEl.value, {
    center: [-5.0916, -42.8034],   // Centro de Teresina
    zoom: 13,
    // Opções de acessibilidade do Leaflet
    keyboard: true,
    zoomControl: true
  })

  // Tile layer OpenStreetMap
  window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors',
    maxZoom: 19
  }).addTo(mapInstance)

  renderizarMarcadores(props.locais)
}

function renderizarMarcadores(locais) {
  if (!mapInstance) return
  const L = window.L

  // Remove marcadores anteriores
  markers.forEach(m => m.remove())
  markers.clear()

  locais.forEach(local => {
    const icone = criarIcone(local.classificacao.nivel)

    const marker = L.marker([local.lat, local.lng], {
      icon: icone,
      // title é lido por tecnologias assistivas no ícone do mapa
      title: `${local.nome} — ${local.classificacao.label}`,
      alt: `Marcador: ${local.nome}, ${local.classificacao.label}`
    })
      .addTo(mapInstance)
      .bindPopup(criarPopupHtml(local), {
        maxWidth: 280,
        className: 'popup-govbr'
      })
      .on('click', () => {
        emit('selecionar', local)
      })

    markers.set(local.id, marker)
  })
}

function centralizarEmLocal(local) {
  if (!mapInstance || !local) return
  mapInstance.setView([local.lat, local.lng], 16, { animate: true })
  const marker = markers.get(local.id)
  if (marker) marker.openPopup()
}

// Observa mudanças nos locais filtrados → re-renderiza marcadores
watch(
  () => props.locais,
  (novosLocais) => { renderizarMarcadores(novosLocais) },
  { deep: true }
)

// Centraliza quando um local é selecionado externamente
watch(
  () => props.localSelecionado,
  (novoLocal) => { if (novoLocal) centralizarEmLocal(novoLocal) }
)

// Quando troca para visualização mapa, re-inicializa se necessário
watch(visualizacao, async (nova) => {
  if (nova === 'mapa' && !mapInstance) {
    await inicializarMapa()
  } else if (nova === 'mapa' && mapInstance) {
    // Leaflet precisa invalidar o tamanho após display:none → block
    await nextTick()
    mapInstance.invalidateSize()
  }
})

onMounted(inicializarMapa)

onUnmounted(() => {
  if (mapInstance) {
    mapInstance.remove()
    mapInstance = null
  }
})
</script>

<style scoped>
.mapa-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.mapa-controles {
  display: flex;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-gray-10);
}
.mapa-controles .br-button {
  padding: var(--space-2) var(--space-4);
  font-size: var(--font-size-sm);
}

.mapa-contador {
  padding: var(--space-2) var(--space-4);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  background: var(--color-gray-05);
  border-bottom: 1px solid var(--color-gray-10);
}

/* Mapa Leaflet */
.mapa-container {
  flex: 1;
  position: relative;
}
.mapa-leaflet {
  width: 100%;
  height: 100%;
  min-height: 400px;
}

/* Legenda */
.mapa-legenda {
  position: absolute;
  bottom: var(--space-6);
  left: var(--space-4);
  z-index: 1000;
  background: white;
  border-radius: var(--radius-md);
  padding: var(--space-3) var(--space-4);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--color-gray-10);
  font-size: var(--font-size-xs);
}
.mapa-legenda__titulo {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-secondary);
  margin-bottom: var(--space-2);
}
.mapa-legenda__lista { list-style: none; display: flex; flex-direction: column; gap: var(--space-1); }
.mapa-legenda__item { display: flex; align-items: center; gap: var(--space-2); }
.mapa-legenda__dot {
  width: 12px; height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}
.dot-total   { background: var(--color-accessible-green); }
.dot-parcial { background: var(--color-warning-dark); }
.dot-nao     { background: var(--color-accessible-red); }

/* Tabela acessível */
.mapa-tabela-wrapper {
  flex: 1;
  overflow: auto;
}
.mapa-tabela {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--font-size-sm);
}
.mapa-tabela th,
.mapa-tabela td {
  padding: var(--space-3) var(--space-4);
  text-align: left;
  border-bottom: 1px solid var(--color-gray-10);
  white-space: nowrap;
}
.mapa-tabela th {
  background: var(--color-gray-05);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-secondary);
  font-size: var(--font-size-xs);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  position: sticky;
  top: 0;
  z-index: 10;
}
.mapa-tabela__row {
  cursor: pointer;
  transition: background var(--transition-fast);
}
.mapa-tabela__row:hover,
.mapa-tabela__row:focus {
  background: var(--color-primary-lightest);
  outline: 2px solid var(--color-primary-default);
  outline-offset: -2px;
}
.mapa-tabela__nome { font-weight: var(--font-weight-semibold); white-space: normal; }
.mapa-tabela__recurso { text-align: center; }
.text-sim { color: var(--color-accessible-green); font-weight: 700; }
.text-nao { color: var(--color-accessible-red); }

.mapa-tabela__btn {
  padding: var(--space-1) var(--space-3) !important;
  font-size: var(--font-size-xs) !important;
  min-height: unset !important;
}
</style>

<style>
/* Popup customizado — escapa do scoped */
.popup-govbr .leaflet-popup-content-wrapper {
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0,0,0,.15);
  border: 1px solid #E8E8E8;
}
.popup-govbr .leaflet-popup-tip { background: white; }

/* Ícone do marcador SVG sem background padrão */
.mapa-marcador { background: none !important; border: none !important; }
</style>
