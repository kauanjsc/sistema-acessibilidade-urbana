<template>
  <div class="home">

    <!-- ─── HERO ───────────────────────────────────────────── -->
    <!--
      <section> semântico com aria-labelledby ligado ao h1.
      Garante que leitores de tela identifiquem a seção (WCAG 1.3.1).
    -->
    <section class="hero" aria-labelledby="hero-heading">
      <div class="container hero__inner">

        <div class="hero__content">
          <p class="hero__pretitulo" aria-hidden="true">
            Prefeitura de Teresina — PI
          </p>
          <h1 id="hero-heading" class="hero__titulo">
            Teresina<br />
            <span class="hero__titulo-destaque">Acessível</span>
          </h1>
          <p class="hero__subtitulo">
            Plataforma de mapeamento urbano de acessibilidade para
            pessoas com deficiência em Teresina, Piauí.
            Encontre locais com rampas, banheiros adaptados, vagas PCD e muito mais.
          </p>

          <!-- Busca principal -->
          <div class="hero__busca">
            <BuscaLocal
              label="Buscar local acessível em Teresina"
              placeholder="Ex.: Hospital, Shopping, Praça da Liberdade..."
              @select="irParaMapa"
              @search="buscarNoMapa"
            />
          </div>

          <div class="hero__acoes">
            <RouterLink to="/mapa" class="br-button primary hero__cta">
              <component :is="lucideIcons.Map" :size="20" aria-hidden="true" style="margin-right: 8px" />
              Explorar o Mapa
            </RouterLink>
            <a href="#sobre" class="br-button secondary">
              Saiba Mais
            </a>
          </div>
        </div>

        <!-- Estatísticas rápidas -->
        <div class="hero__stats" role="region" aria-label="Estatísticas da plataforma">
          <div
            v-for="stat in estatisticas"
            :key="stat.label"
            class="hero__stat-card"
          >
            <span class="hero__stat-numero" :style="{ color: stat.cor }" aria-hidden="true">
              {{ stat.valor }}
            </span>
            <span class="hero__stat-label">{{ stat.label }}</span>
          </div>
        </div>

      </div>
    </section>

    <!-- ─── COMO USAR ──────────────────────────────────────── -->
    <section class="como-usar" aria-labelledby="como-usar-heading" id="sobre">
      <div class="container">
        <h2 id="como-usar-heading" class="section-titulo">Como usar a plataforma</h2>
        <p class="section-subtitulo">
          Três passos simples para encontrar locais acessíveis em Teresina.
        </p>

        <ol class="passos" role="list">
          <li v-for="passo in passos" :key="passo.numero" class="passo">
            <div class="passo__numero" aria-hidden="true">
              <component :is="lucideIcons[passo.icone]" :size="20" />
            </div>
            <div>
              <h3 class="passo__titulo">{{ passo.titulo }}</h3>
              <p class="passo__desc">{{ passo.desc }}</p>
            </div>
          </li>
        </ol>
      </div>
    </section>

    <!-- ─── CLASSIFICAÇÃO ─────────────────────────────────── -->
    <section class="classificacao-section" aria-labelledby="classif-heading">
      <div class="container">
        <h2 id="classif-heading" class="section-titulo">Sistema de Classificação</h2>
        <p class="section-subtitulo">
          Cada local recebe uma classificação baseada nos recursos de acessibilidade disponíveis.
        </p>

        <div class="classif-cards">
          <div 
            v-for="nivel in niveisInfo" 
            :key="nivel.chave" 
            class="classif-card" 
            :class="`classif-card--${nivel.chave}`"
          >
            <component
              :is="lucideIcons[nivel.icone]"
              :size="44"
              :stroke-width="1.5"
              class="classif-card__icone-lucide"
              :class="`text-${nivel.chave}`"
              aria-hidden="true"
            />
            
            <h3 class="classif-card__titulo">{{ nivel.label }}</h3>
            <p class="classif-card__desc">{{ nivel.desc }}</p>
            
            <BadgeAcessibilidade
              :nivel="nivel.chave"
              :label="nivel.label"
            />
          </div>
        </div>
      </div>
    </section>

    <!--  RECURSOS MAPEADOS  -->
    <section class="recursos-section" aria-labelledby="recursos-heading">
      <div class="container">
        <h2 id="recursos-heading" class="section-titulo">Recursos Mapeados</h2>
        <p class="section-subtitulo">
          Verificamos a presença dos seguintes recursos em cada local cadastrado.
        </p>

        <ul class="recursos-grid" role="list">
          <li v-for="(meta, chave) in RECURSOS_META" :key="chave" class="recurso-card">
            <component
              :is="lucideIcons[meta.icone]"
              :size="28"
              stroke-width="1.5"
              class="recurso-card__icone-lucide"
              aria-hidden="true"
            />
            <h3 class="recurso-card__label">{{ meta.label }}</h3>
            <p class="recurso-card__desc">{{ meta.descricao }}</p>
          </li>
        </ul>
      </div>
    </section>

    <!-- ---- CTA MAPA ----- -->
    <section class="cta-section" aria-labelledby="cta-heading">
      <div class="container cta-inner">
        <div>
          <h2 id="cta-heading" class="cta-titulo">
            Pronto para explorar Teresina?
          </h2>
          <p class="cta-desc">
            Acesse o mapa interativo com {{ totalLocais }} locais cadastrados.
          </p>
        </div>
        <RouterLink to="/mapa" class="br-button primary cta-btn">
          <component
            :is="lucideIcons.Map"
            :size="20"
            aria-hidden="true"
            style="margin-right: 8px"
          />
          Ir para o Mapa
        </RouterLink>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BuscaLocal from '@/components/BuscaLocal.vue'
import * as lucideIcons from 'lucide-vue-next'
import BadgeAcessibilidade from '@/components/BadgeAcessibilidade.vue'
import { getLocais, RECURSOS_META, classificarAcessibilidade } from '@/services/acessibilidadeService.js'

const router = useRouter()
const todosLocais = ref([])

onMounted(async () => {
  try {
    todosLocais.value = await getLocais()
  } catch (err) {
    console.error('[HomeView] erro ao carregar locais:', err)
  }
})

const totalLocais = computed(() => todosLocais.value.length)

// ── Estatísticas 
const totalAcessiveis = computed(() =>
  todosLocais.value.filter(l => classificarAcessibilidade(l) === 'alto').length
)
const totalParciais = computed(() =>
  todosLocais.value.filter(l => classificarAcessibilidade(l) === 'medio').length
)

const estatisticas = computed(() => [
  { valor: totalLocais.value, label: 'Locais Mapeados', cor: 'var(--color-primary-default)' },
  { valor: totalAcessiveis.value, label: 'Totalmente Acessíveis', cor: 'var(--color-accessible-green)' },
  { valor: totalParciais.value, label: 'Parcialmente Acessíveis', cor: 'var(--color-warning-dark)' }
])

//  Passos ------
const passos = [
  {
    numero: '1',
    icone: 'Search',
    titulo: 'Busque ou navegue pelo mapa',
    desc: 'Use o campo de busca para encontrar um local específico ou explore o mapa interativo de Teresina.'
  },
  {
    numero: '2',
    icone: 'Filter',
    titulo: 'Aplique filtros de acessibilidade',
    desc: 'Filtre os locais pelos recursos que você precisa: rampa, banheiro adaptado, vaga PCD e mais.'
  },
  {
    numero: '3',
    icone: 'Info',
    titulo: 'Veja os detalhes completos',
    desc: 'Clique em um marcador para ver todos os recursos de acessibilidade disponíveis no local.'
  }
]

// ── Níveis ---------
const niveisInfo = [
  {
    chave: 'total',
    icone: 'CheckCircle2',
    label: 'Totalmente Acessível',
    desc: 'Possui 5 ou 6 dos recursos de acessibilidade verificados.'
  },
  {
    chave: 'parcial',
    icone: 'AlertCircle',
    label: 'Parcialmente Acessível',
    desc: 'Possui de 2 a 4 recursos de acessibilidade disponíveis.'
  },
  {
    chave: 'nao',
    icone: 'XCircle',
    label: 'Não Acessível',
    desc: 'Possui 0 ou 1 recurso de acessibilidade disponível.'
  }
]

// ── Navegação -------------
function irParaMapa(local) {
  router.push({ name: 'mapa', query: { id: local.id } })
}

function buscarNoMapa(query) {
  if (query) router.push({ name: 'mapa', query: { busca: query } })
}
</script>

<style scoped>
/* Cores dos ícones de classificação */
.text-total { color: var(--color-accessible-green); }
.text-parcial { color: var(--color-warning-dark); }
.text-nao { color: var(--color-accessible-red); }

.classif-card__icone-lucide {
  margin-bottom: var(--space-2);
}

.recurso-card__icone-lucide {
  color: var(--color-primary-default);
  margin-bottom: var(--space-2);
}

.hero {
  background: linear-gradient(135deg, var(--color-primary-darker) 0%, var(--color-primary-default) 60%, var(--color-primary-light) 100%);
  color: var(--color-white);
  padding: var(--space-16) 0 var(--space-12);
}
.hero__inner {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: var(--space-12);
  align-items: start;
}
.hero__pretitulo {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  opacity: 0.75;
  margin-bottom: var(--space-3);
}
.hero__titulo {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: var(--font-weight-extrabold);
  line-height: 1.05;
  color: var(--color-white);
  margin-bottom: var(--space-4);
}
.hero__titulo-destaque {
  color: var(--color-warning);
}
.hero__subtitulo {
  font-size: var(--font-size-lg);
  line-height: var(--line-height-relaxed);
  opacity: 0.9;
  max-width: 560px;
  margin-bottom: var(--space-8);
}
.hero__busca {
  max-width: 560px;
  margin-bottom: var(--space-6);
}
.hero__acoes {
  display: flex;
  gap: var(--space-3);
  flex-wrap: wrap;
}
.hero__cta {
  background: var(--color-warning) !important;
  border-color: var(--color-warning) !important;
  color: var(--color-primary-darker) !important;
  font-weight: var(--font-weight-bold) !important;
}
.hero__cta:hover {
  background: #e6b800 !important;
  border-color: #e6b800 !important;
}

/* Stats */
.hero__stats {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  flex-shrink: 0;
}
.hero__stat-card {
  background: rgba(255,255,255,.12);
  border: 1px solid rgba(255,255,255,.2);
  border-radius: var(--radius-md);
  padding: var(--space-4) var(--space-6);
  text-align: center;
  min-width: 140px;
  backdrop-filter: blur(4px);
}
.hero__stat-numero {
  display: block;
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-extrabold);
  line-height: 1;
  margin-bottom: var(--space-1);
}
.hero__stat-label {
  font-size: var(--font-size-xs);
  opacity: 0.85;
  font-weight: var(--font-weight-medium);
}

/* ── SEÇÕES ------- */
.section-titulo {
  font-size: var(--font-size-2xl);
  color: var(--color-primary-dark);
  margin-bottom: var(--space-2);
}
.section-subtitulo {
  font-size: var(--font-size-md);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-8);
  max-width: 600px;
}

.como-usar {
  padding: var(--space-12) 0;
  background: var(--color-surface);
}
.passos { list-style: none; display: flex; flex-direction: column; gap: var(--space-6); max-width: 640px; }
.passo { display: flex; gap: var(--space-4); align-items: flex-start; }
.passo__numero {
  width: 40px; height: 40px;
  background: var(--color-primary-default);
  color: white;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-lg);
  flex-shrink: 0;
}
.passo__titulo { font-size: var(--font-size-md); font-weight: var(--font-weight-bold); margin-bottom: var(--space-1); }
.passo__desc { font-size: var(--font-size-sm); color: var(--color-text-secondary); margin-bottom: 0; }

/* ── CLASSIFICAÇÃO ----------- */
.classificacao-section { padding: var(--space-12) 0; background: var(--color-gray-05); }
.classif-cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-6); }
.classif-card {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: var(--space-6);
  border: 1px solid var(--color-gray-10);
  display: flex; flex-direction: column; gap: var(--space-3);
  box-shadow: var(--shadow-sm);
}
.classif-card--total   { border-top: 4px solid var(--color-accessible-green); }
.classif-card--parcial { border-top: 4px solid var(--color-warning-dark); }
.classif-card--nao     { border-top: 4px solid var(--color-accessible-red); }
.classif-card__icone { font-size: 2rem; }
.classif-card__titulo { font-size: var(--font-size-md); font-weight: var(--font-weight-bold); }
.classif-card__desc { font-size: var(--font-size-sm); color: var(--color-text-secondary); flex: 1; margin-bottom: 0; }

/* ── RECURSOS ------------ */
.recursos-section { padding: var(--space-12) 0; background: var(--color-surface); }
.recursos-grid {
  list-style: none;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: var(--space-4);
}
.recurso-card {
  background: var(--color-gray-05);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  border: 1px solid var(--color-gray-10);
  display: flex; flex-direction: column; gap: var(--space-2);
  transition: box-shadow var(--transition-base);
}
.recurso-card:hover { box-shadow: var(--shadow-sm); }
.recurso-card__icone { font-size: 1.75rem; }
.recurso-card__label { font-size: var(--font-size-sm); font-weight: var(--font-weight-bold); }
.recurso-card__desc { font-size: var(--font-size-xs); color: var(--color-text-secondary); margin-bottom: 0; }

/* --- CTA -------------- */
.cta-section {
  padding: var(--space-12) 0;
  background: var(--color-primary-darker);
}
.cta-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-8);
  flex-wrap: wrap;
}
.cta-titulo {
  font-size: var(--font-size-2xl);
  color: var(--color-white);
  margin-bottom: var(--space-2);
}
.cta-desc { color: rgba(255,255,255,.75); margin-bottom: 0; }
.cta-btn {
  background: var(--color-warning) !important;
  border-color: var(--color-warning) !important;
  color: var(--color-primary-darker) !important;
  font-weight: var(--font-weight-bold) !important;
  white-space: nowrap;
}

/* --- RESPONSIVO ----- */
@media (max-width: 900px) {
  .hero__inner { grid-template-columns: 1fr; }
  .hero__stats { flex-direction: row; justify-content: center; }
  .hero__stat-card { min-width: 100px; }
  .classif-cards { grid-template-columns: 1fr; }
}
@media (max-width: 640px) {
  .hero { padding: var(--space-10) 0; }
  .hero__acoes { flex-direction: column; }
  .hero__stats { flex-direction: column; }
  .cta-inner { flex-direction: column; text-align: center; }
}
</style>