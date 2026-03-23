<template>
  <section class="lista-comentarios" aria-labelledby="lista-comentarios-titulo">

    <!-- Cabeçalho -->
    <div class="lista-comentarios__header">
      <h3 id="lista-comentarios-titulo" class="lista-comentarios__titulo">
        <span aria-hidden="true">💬</span>
        Avaliações da Comunidade
        <span v-if="comentarios.length > 0" class="lista-comentarios__badge">
          {{ comentarios.length }}
        </span>
      </h3>

      <!-- Termômetro -->
      <div v-if="comentarios.length > 0" class="lista-comentarios__termometro">
        <div class="lista-comentarios__termometro-barra">
          <div
            class="lista-comentarios__termometro-fill"
            :style="{ width: percentualAcessivel + '%' }"
          ></div>
        </div>
        <div class="lista-comentarios__termometro-info">
          <span class="text-acessivel">✅ {{ totalAcessiveis }} acessível{{ totalAcessiveis !== 1 ? 'is' : '' }}</span>
          <span aria-hidden="true"> · </span>
          <span class="text-nao-acessivel">❌ {{ totalBarreiras }} com barreiras</span>
          <span aria-hidden="true"> · </span>
          <span class="text-percentual">{{ percentualAcessivel }}% positivo</span>
        </div>
      </div>
    </div>

    <!-- Carregando -->
    <div v-if="carregando" class="lista-comentarios__carregando" role="status" aria-live="polite">
      <span aria-hidden="true">⟳</span> Carregando avaliações...
    </div>

    <!-- Vazio -->
    <div v-if="!carregando && comentarios.length === 0" class="lista-comentarios__vazio">
      <span class="lista-comentarios__vazio-icone">📭</span>
      <p class="lista-comentarios__vazio-texto">
        Ainda não há avaliações para este local.<br />Seja o primeiro a contribuir!
      </p>
    </div>

    <!-- Lista -->
    <ul v-else-if="!carregando" class="lista-comentarios__lista">
      <li
        v-for="av in visiveis"
        :key="av.id"
        class="lista-comentarios__item"
        :class="av.acessivel ? 'item-acessivel' : 'item-barreira'"
      >
        <div class="lista-comentarios__item-header">
          <span class="lista-comentarios__status" :class="av.acessivel ? 'status-sim' : 'status-nao'">
            {{ av.acessivel ? '✅ Acessível' : '❌ Com barreiras' }}
          </span>
          <div class="lista-comentarios__meta">
            <span>👤 {{ av.autor }}</span>
            <time :datetime="av.data">{{ dataRelativa(av.data) }}</time>
          </div>
        </div>
        <p class="lista-comentarios__texto">{{ av.comentario }}</p>
      </li>
    </ul>

    <!-- Ver mais -->
    <div v-if="!carregando && !verTodos && comentarios.length > limite" class="lista-comentarios__ver-mais">
      <button class="br-button secondary" type="button" @click="verTodos = true">
        Ver todas ({{ comentarios.length - limite }} restantes)
      </button>
    </div>

  </section>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { listarComentarios, avaliacoesStore } from '@/services/avaliacoesService.js'

const props = defineProps({
  localId:  { type: Number, required: true },
  limite:   { type: Number, default: 4 }
})

const verTodos    = ref(false)
const comentarios = ref([])
const carregando  = ref(false)

// Busca comentários da API (ou mock, conforme VITE_USE_MOCK)
async function buscarComentarios() {
  if (!props.localId) return
  try {
    carregando.value = true
    comentarios.value = await listarComentarios(props.localId)
  } catch (err) {
    console.error('[ListaComentarios] erro ao buscar:', err)
    // Fallback: filtra do store local se API falhar
    comentarios.value = avaliacoesStore.value
      .filter(a => Number(a.localId) === Number(props.localId))
      .sort((a, b) => new Date(b.data) - new Date(a.data))
  } finally {
    carregando.value = false
  }
}

// Carrega ao montar e quando o localId muda
onMounted(buscarComentarios)
watch(() => props.localId, () => {
  verTodos.value = false
  buscarComentarios()
})

// Expõe recarregar para o pai chamar após envio de avaliação
defineExpose({ recarregar: buscarComentarios })

const visiveis = computed(() =>
  verTodos.value ? comentarios.value : comentarios.value.slice(0, props.limite)
)

const totalAcessiveis    = computed(() => comentarios.value.filter(a => a.acessivel).length)
const totalBarreiras     = computed(() => comentarios.value.filter(a => !a.acessivel).length)
const percentualAcessivel = computed(() =>
  comentarios.value.length > 0
    ? Math.round((totalAcessiveis.value / comentarios.value.length) * 100)
    : 0
)

function dataRelativa(iso) {
  const dias = Math.floor((Date.now() - new Date(iso)) / 86400000)
  if (dias === 0) return 'Hoje'
  if (dias === 1) return 'Ontem'
  if (dias < 7)  return `Há ${dias} dias`
  if (dias < 30) return `Há ${Math.floor(dias / 7)} semana${Math.floor(dias / 7) > 1 ? 's' : ''}`
  return new Date(iso).toLocaleDateString('pt-BR', { day:'2-digit', month:'short', year:'numeric' })
}
</script>

<style scoped>
.lista-comentarios { display: flex; flex-direction: column; gap: var(--space-4); }

.lista-comentarios__header {
  display: flex; flex-direction: column; gap: var(--space-3);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--color-gray-10);
}
.lista-comentarios__titulo {
  font-size: var(--font-size-lg); color: var(--color-primary-dark);
  display: flex; align-items: center; gap: var(--space-2);
}
.lista-comentarios__badge {
  background: var(--color-primary-default); color: var(--color-white);
  font-size: var(--font-size-xs); font-weight: var(--font-weight-bold);
  padding: 2px 8px; border-radius: 999px; min-width: 22px; text-align: center;
}

.lista-comentarios__termometro { display: flex; flex-direction: column; gap: var(--space-2); }
.lista-comentarios__termometro-barra {
  height: 10px; background: #fecdd3;
  border-radius: 999px; overflow: hidden;
}
.lista-comentarios__termometro-fill {
  height: 100%; background: #168821;
  border-radius: 999px; transition: width 500ms ease; min-width: 4px;
}
.lista-comentarios__termometro-info {
  display: flex; align-items: center; flex-wrap: wrap;
  gap: var(--space-2); font-size: var(--font-size-xs);
}
.text-acessivel     { color: #168821; font-weight: 600; }
.text-nao-acessivel { color: #c0392b; font-weight: 600; }
.text-percentual    { color: var(--color-text-secondary); }

.lista-comentarios__vazio {
  display: flex; flex-direction: column; align-items: center;
  gap: var(--space-3); padding: 2rem var(--space-6);
  text-align: center; color: var(--color-text-secondary);
  background: var(--color-gray-05); border-radius: var(--radius-md);
  border: 1px dashed var(--color-gray-20);
}
.lista-comentarios__vazio-icone { font-size: 2.5rem; }
.lista-comentarios__vazio-texto { font-size: var(--font-size-sm); line-height: 1.6; margin: 0; }

.lista-comentarios__lista { list-style: none; display: flex; flex-direction: column; gap: var(--space-3); }

.lista-comentarios__item {
  background: #fff; border: 1px solid #e5e7eb;
  border-radius: var(--radius-md); padding: var(--space-4);
  display: flex; flex-direction: column; gap: var(--space-3);
}
.item-acessivel { border-left: 4px solid #168821; }
.item-barreira  { border-left: 4px solid #c0392b; }

.lista-comentarios__item-header {
  display: flex; align-items: center;
  justify-content: space-between; flex-wrap: wrap; gap: var(--space-2);
}
.lista-comentarios__status {
  font-size: var(--font-size-xs); font-weight: 700;
  padding: 2px 10px; border-radius: 999px;
}
.status-sim { background: #d1fae5; color: #168821; border: 1px solid #168821; }
.status-nao { background: #fee2e2; color: #c0392b; border: 1px solid #c0392b; }

.lista-comentarios__meta {
  display: flex; align-items: center; gap: var(--space-3);
  font-size: var(--font-size-xs); color: var(--color-text-secondary);
}

.lista-comentarios__texto {
  font-size: var(--font-size-sm); color: var(--color-text-primary);
  line-height: 1.6; margin: 0;
}

.lista-comentarios__ver-mais { display: flex; justify-content: center; padding-top: var(--space-2); }

.lista-comentarios__carregando {
  padding: var(--space-6);
  text-align: center;
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
}
.lista-comentarios__carregando span {
  display: inline-block;
  animation: spin-lista 1s linear infinite;
}
@keyframes spin-lista { to { transform: rotate(360deg); } }
</style>