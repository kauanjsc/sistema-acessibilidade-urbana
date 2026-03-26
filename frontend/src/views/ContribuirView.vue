<template>
  <div class="contribuir-view">

    <!-- ─── HERO DA PÁGINA ──────────────────────────────── -->
    <div class="contribuir-hero" role="banner">
      <div class="container contribuir-hero__inner">
        <div>
          <p class="contribuir-hero__pretitulo" aria-hidden="true">
            Participação Cidadã
          </p>
          <h1 id="contribuir-titulo" class="contribuir-hero__titulo">
            Contribua com a
            <span class="contribuir-hero__destaque">Teresina Acessível</span>
          </h1>
          <p class="contribuir-hero__desc">
            Você conhece um local em Teresina? Registre sua experiência sobre
            acessibilidade e ajude outras pessoas com deficiência a planejar seus trajetos.
          </p>
        </div>

        <!-- Stats rápidas -->
        <div class="contribuir-hero__stats" aria-label="Estatísticas de contribuições">
          <div class="contribuir-hero__stat">
            <span class="contribuir-hero__stat-num">{{ totalContribuicoes }}</span>
            <span class="contribuir-hero__stat-label">Contribuições</span>
          </div>
          <div class="contribuir-hero__stat">
            <span class="contribuir-hero__stat-num">{{ totalLocais }}</span>
            <span class="contribuir-hero__stat-label">Locais mapeados</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ─── CONTEÚDO PRINCIPAL ──────────────────────────── -->
    <div class="container contribuir-main">

      <!-- PASSO 1: Selecione o local ──────────────────── -->
      <section
        class="contribuir-passo"
        aria-labelledby="passo1-titulo"
      >
        <div class="contribuir-passo__header">
          <span class="contribuir-passo__num" aria-hidden="true">1</span>
          <h2 id="passo1-titulo" class="contribuir-passo__titulo">
            Selecione o local
          </h2>
        </div>

        <div class="contribuir-passo__corpo">

          <!-- Busca / seleção de local ──────────────── -->
          <div class="contribuir-busca-wrapper">
            <BuscaLocal
              label="Buscar local para avaliar"
              placeholder="Digite o nome do local, bairro ou tipo..."
              @select="selecionarLocal"
              @search="onBuscaChange"
            />
          </div>

          <!-- Ou selecione por tipo ──────────────────── -->
          <div class="contribuir-filtro-tipo">
            <label for="filtro-tipo" class="contribuir-label">
              Ou filtre por tipo de local:
            </label>
            <select
              id="filtro-tipo"
              v-model="tipoFiltro"
              class="br-input contribuir-select"
              aria-label="Filtrar locais por tipo de estabelecimento"
            >
              <option value="">Todos os tipos</option>
              <option v-for="(meta, key) in TIPOS_META" :key="key" :value="key">
                {{ meta.label }}
              </option>
            </select>
          </div>

          <!-- Lista rápida de locais ─────────────────── -->
          <div
            v-if="locaisFiltrados.length > 0"
            class="contribuir-lista-locais"
            role="group"
            aria-label="Selecione um local da lista para avaliar"
          >
            <p class="contribuir-lista-locais__instrucao" aria-live="polite">
              {{ locaisFiltrados.length }} local{{ locaisFiltrados.length !== 1 ? 'is' : '' }} disponível{{ locaisFiltrados.length !== 1 ? 'is' : '' }}
            </p>

            <ul role="list" class="contribuir-locais-grid">
              <li
                v-for="local in locaisVisiveis"
                :key="local.id"
              >
                <button
                  type="button"
                  class="contribuir-local-card"
                  :class="{
                    'is-selecionado': localSelecionado?.id === local.id
                  }"
                  :aria-pressed="localSelecionado?.id === local.id"
                  :aria-label="`Selecionar ${local.nome}, ${local.tipoLabel}, ${local.bairro}. Nível de acessibilidade: ${local.classificacao.label}`"
                  @click="selecionarLocal(local)"
                >
                  <div class="contribuir-local-card__body">
                    <p class="contribuir-local-card__tipo">{{ local.tipoLabel }}</p>
                    <p class="contribuir-local-card__nome">{{ local.nome }}</p>
                    <p class="contribuir-local-card__end">
                      <MapPin aria-hidden="true" :size="14" style="margin-right: 4px;" />
                       {{ local.bairro }}
                    </p>
                  </div>
                  <BadgeAcessibilidade
                    :nivel="local.classificacao.nivel"
                    :label="local.classificacao.label"
                  />
                </button>
              </li>
            </ul>

            <!-- Ver mais locais -->
            <div v-if="locaisFiltrados.length > limiteLista" class="contribuir-ver-mais">
              <button
                v-if="!verTodosLocais"
                class="br-button tertiary"
                type="button"
                @click="verTodosLocais = true"
              >
                Ver todos os {{ locaisFiltrados.length }} locais
              </button>
              <button
                v-else
                class="br-button tertiary"
                type="button"
                @click="verTodosLocais = false"
              >
                Mostrar menos
              </button>
            </div>
          </div>

        </div>
      </section>

      <!-- PASSO 2: Formulário + comentários ──────────── -->
      <section
        class="contribuir-passo"
        :class="{ 'is-bloqueado': !localSelecionado }"
        aria-labelledby="passo2-titulo"
      >
        <div class="contribuir-passo__header">
          <span class="contribuir-passo__num" aria-hidden="true">2</span>
          <h2 id="passo2-titulo" class="contribuir-passo__titulo">
            Avalie a acessibilidade
          </h2>
        </div>

        <!-- Aviso quando nenhum local está selecionado -->
        <div
          v-if="!localSelecionado"
          class="contribuir-aviso"
          role="status"
          aria-live="polite"
        >
          <MousePointerClick aria-hidden="true" :size="20" />
          Selecione um local no passo 1 para habilitar a avaliação.
        </div>

        <div v-else class="contribuir-passo__corpo contribuir-passo__corpo--cols">

          <!-- Coluna esquerda: formulário ────────────── -->
          <div class="contribuir-col-form">
            <FormAvaliacaoLocal
              :local="localSelecionado"
              @enviado="onAvaliacaoEnviada"
            />
          </div>

          <!-- Coluna direita: comentários existentes ── -->
          <div class="contribuir-col-comentarios">
            <ListaComentarios
              ref="listaRef"
              :local-id="localSelecionado.id"
            />
          </div>

        </div>
      </section>

    </div>

    <!-- ─── COMO FUNCIONA ─────────────────────────────── -->
    <section class="contribuir-info" aria-labelledby="como-funciona-titulo">
      <div class="container">
        <h2 id="como-funciona-titulo" class="section-titulo">
          Como funciona a Contribuição Cidadã?
        </h2>

        <ol class="contribuir-passos-info" role="list">
          <li v-for="info in comoFunciona" :key="info.numero" class="contribuir-passo-info">
            <component :is="info.icone" class="contribuir-passo-info__num" aria-hidden="true" :size="28" />
            <div>
              <h3 class="contribuir-passo-info__titulo">{{ info.titulo }}</h3>
              <p class="contribuir-passo-info__desc">{{ info.desc }}</p>
            </div>
          </li>
        </ol>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import BuscaLocal from '@/components/BuscaLocal.vue'
import BadgeAcessibilidade from '@/components/BadgeAcessibilidade.vue'
import FormAvaliacaoLocal from '@/components/FormAvaliacaoLocal.vue'
import ListaComentarios from '@/components/ListaComentarios.vue'
import { MapPin, MousePointerClick, Search, Pencil, Send, Map as MapIcon } from 'lucide-vue-next'
import {
  getLocais,
  filtrarPorBusca,
  TIPOS_META
} from '@/services/acessibilidadeService.js'
import { totalAvaliacoes } from '@/services/avaliacoesService.js'

const route = useRoute()

// ── Dados ─────────────────────────────────────────────────────
const todosLocais      = ref([])
const carregando       = ref(true)
const limiteLista      = 8
const busca            = ref('')
const tipoFiltro       = ref('')
const localSelecionado = ref(null)
const verTodosLocais   = ref(false)
const listaRef         = ref(null)

const totalLocais        = computed(() => todosLocais.value.length)
const totalContribuicoes = totalAvaliacoes

// ── Filtros ───────────────────────────────────────────────────
const locaisFiltrados = computed(() => {
  let lista = todosLocais.value
  if (busca.value) lista = filtrarPorBusca(lista, busca.value)
  if (tipoFiltro.value) lista = lista.filter(l => l.tipo === tipoFiltro.value)
  return lista
})

const locaisVisiveis = computed(() =>
  verTodosLocais.value ? locaisFiltrados.value : locaisFiltrados.value.slice(0, limiteLista)
)

// ── Carrega locais e trata pré-seleção via query param ────────
onMounted(async () => {
  try {
    carregando.value = true
    todosLocais.value = await getLocais()

    if (route.query.id) {
      const local = todosLocais.value.find(l => l.id === Number(route.query.id))
      if (local) localSelecionado.value = local
    }
  } catch (err) {
    console.error('[ContribuirView] erro ao carregar locais:', err)
  } finally {
    carregando.value = false
  }
})

// ── Handlers ─────────────────────────────────────────────────
function selecionarLocal(local) {
  localSelecionado.value = local
  // Rola suavemente para o passo 2
  setTimeout(() => {
    document.getElementById('passo2-titulo')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }, 100)
}

function onBuscaChange(query) {
  busca.value = query
}

function onAvaliacaoEnviada(avaliacao) {
  
  // Força reload da lista de comentários
  listaRef.value?.recarregar()
}

// ── Conteúdo estático ────────────────────────────────────────
const comoFunciona = [
  {
    numero: 1,
    icone: Search,
    titulo: 'Encontre o local',
    desc: 'Busque pelo nome do local, bairro ou filtre pelo tipo de estabelecimento.'
  },
  {
    numero: 2,
    icone: Pencil,
    titulo: 'Avalie a acessibilidade',
    desc: 'Informe se o local é acessível e descreva o que você observou: rampas, banheiros, calçadas, etc.'
  },
  {
    numero: 3,
    icone: Send,
    titulo: 'Envie sua contribuição',
    desc: 'Sua avaliação fica disponível para todos que consultarem o local no mapa.'
  },
  {
    numero: 4,
    icone: MapIcon,
    titulo: 'Impacto no mapa',
    desc: 'O índice cidadão de cada local é calculado com base nas contribuições da comunidade.'
  }
]
</script>

<style scoped>
/* ── HERO ────────────────────────────────────────────────────── */
.contribuir-hero {
  background: linear-gradient(135deg, var(--color-primary-darker) 0%, var(--color-primary-dark) 60%, var(--color-primary-default) 100%);
  color: var(--color-white);
  padding: var(--space-12) 0 var(--space-10);
}
.contribuir-hero__inner {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: var(--space-10);
  align-items: center;
}
.contribuir-hero__pretitulo {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  opacity: 0.75;
  margin-bottom: var(--space-2);
}
.contribuir-hero__titulo {
  font-size: clamp(1.75rem, 4vw, 3rem);
  font-weight: var(--font-weight-extrabold);
  line-height: 1.1;
  color: var(--color-white);
  margin-bottom: var(--space-4);
}
.contribuir-hero__destaque { color: var(--color-warning); }
.contribuir-hero__desc {
  font-size: var(--font-size-md);
  opacity: 0.9;
  line-height: var(--line-height-relaxed);
  max-width: 560px;
  margin-bottom: 0;
}

.contribuir-hero__stats {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  flex-shrink: 0;
}
.contribuir-hero__stat {
  text-align: center;
  background: rgba(255,255,255,.12);
  border: 1px solid rgba(255,255,255,.2);
  border-radius: var(--radius-md);
  padding: var(--space-4) var(--space-6);
  min-width: 120px;
}
.contribuir-hero__stat-num {
  display: block;
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-extrabold);
  color: var(--color-warning);
  line-height: 1;
  margin-bottom: var(--space-1);
}
.contribuir-hero__stat-label {
  font-size: var(--font-size-xs);
  opacity: 0.85;
  font-weight: var(--font-weight-medium);
}

/* ── MAIN ────────────────────────────────────────────────────── */
.contribuir-main {
  padding: var(--space-10) var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-12);
}

/* ── PASSOS ──────────────────────────────────────────────────── */
.contribuir-passo {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
  transition: opacity var(--transition-base);
}
.contribuir-passo.is-bloqueado { opacity: 0.6; }

.contribuir-passo__header {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}
.contribuir-passo__num {
  width: 44px;
  height: 44px;
  background: var(--color-primary-default);
  color: var(--color-white);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--font-weight-extrabold);
  font-size: var(--font-size-xl);
  flex-shrink: 0;
}
.contribuir-passo__titulo {
  font-size: var(--font-size-2xl);
  color: var(--color-primary-dark);
  margin-bottom: 0;
}
.contribuir-passo__corpo {
  padding-left: calc(44px + var(--space-4));
}
.contribuir-passo__corpo--cols {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-8);
  align-items: start;
}

/* ── BUSCA + FILTRO ──────────────────────────────────────────── */
.contribuir-busca-wrapper { max-width: 560px; margin-bottom: var(--space-4); }
.contribuir-label {
  display: block;
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  margin-bottom: var(--space-2);
}
.contribuir-filtro-tipo { max-width: 320px; margin-bottom: var(--space-4); }
.contribuir-select {
  appearance: auto;
  cursor: pointer;
}

/* ── LISTA DE LOCAIS ─────────────────────────────────────────── */
.contribuir-lista-locais__instrucao {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-3);
}
.contribuir-locais-grid {
  list-style: none;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.contribuir-local-card {
  width: 100%;
  text-align: left;
  background: var(--color-surface);
  border: 2px solid var(--color-gray-10);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  cursor: pointer;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast), background var(--transition-fast);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  min-height: 44px;
}
.contribuir-local-card:hover {
  border-color: var(--color-primary-default);
  background: var(--color-primary-lightest);
  box-shadow: var(--shadow-sm);
}
.contribuir-local-card.is-selecionado {
  border-color: var(--color-primary-default);
  background: var(--color-primary-lightest);
  box-shadow: 0 0 0 3px var(--color-primary-default);
}
.contribuir-local-card__tipo {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-primary-default);
  margin-bottom: 0;
}
.contribuir-local-card__nome {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin-bottom: var(--space-1);
}
.contribuir-local-card__end {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  display: flex;
  align-items: center;
  gap: var(--space-1);
  margin-bottom: 0;
}

.contribuir-ver-mais { display: flex; justify-content: center; }

/* ── AVISO ───────────────────────────────────────────────────── */
.contribuir-aviso {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
  background: var(--color-info-light);
  border: 1px solid var(--color-info);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  color: var(--color-info);
  font-weight: var(--font-weight-medium);
  max-width: 500px;
}

/* ── COLUNAS FORM + LISTA ────────────────────────────────────── */
.contribuir-col-form,
.contribuir-col-comentarios {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

/* ── COMO FUNCIONA ───────────────────────────────────────────── */
.contribuir-info {
  background: var(--color-gray-05);
  padding: var(--space-12) 0;
  border-top: 1px solid var(--color-gray-10);
}
.contribuir-passos-info {
  list-style: none;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--space-6);
  margin-top: var(--space-6);
}
.contribuir-passo-info {
  display: flex;
  gap: var(--space-4);
  align-items: flex-start;
}
.contribuir-passo-info__num { font-size: 1.75rem; flex-shrink: 0; }
.contribuir-passo-info__titulo {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-bold);
  margin-bottom: var(--space-1);
}
.contribuir-passo-info__desc {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-bottom: 0;
  line-height: var(--line-height-relaxed);
}

.section-titulo {
  font-size: var(--font-size-2xl);
  color: var(--color-primary-dark);
}

/* ── RESPONSIVO ──────────────────────────────────────────────── */
@media (max-width: 1024px) {
  .contribuir-passo__corpo--cols {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 768px) {
  .contribuir-hero__inner { grid-template-columns: 1fr; }
  .contribuir-hero__stats { flex-direction: row; }
  .contribuir-passo__corpo { padding-left: 0; }
}
@media (max-width: 480px) {
  .contribuir-hero__stats { flex-direction: column; }
  .contribuir-locais-grid { grid-template-columns: 1fr; }
}
</style>