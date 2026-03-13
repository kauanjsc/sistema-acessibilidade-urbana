<template>
  <aside
    class="painel-detalhes"
    :class="{ 'is-open': local }"
    role="complementary"
    aria-label="Detalhes do local selecionado"
    :aria-hidden="!local"
  >

    <!-- Estado vazio -->
    <div v-if="!local" class="painel-detalhes__vazio" aria-live="polite">
      <span aria-hidden="true" class="painel-detalhes__vazio-icon">📍</span>
      <p>Selecione um local no mapa para ver os detalhes de acessibilidade.</p>
    </div>

    <!-- Conteúdo do local -->
    <div v-else class="painel-detalhes__conteudo" aria-live="polite" aria-atomic="true">

      <!-- Cabeçalho -->
      <div class="painel-detalhes__header">
        <div class="painel-detalhes__header-top">
          <span class="painel-detalhes__tipo-tag">
            {{ local.tipoLabel }}
          </span>
          <button
            class="br-button tertiary painel-detalhes__fechar"
            type="button"
            aria-label="Fechar painel de detalhes"
            @click="$emit('fechar')"
          >
            <span aria-hidden="true">✕</span>
          </button>
        </div>

        <h2 :id="`local-${local.id}-titulo`" class="painel-detalhes__nome">
          {{ local.nome }}
        </h2>

        <p class="painel-detalhes__endereco">
          <span aria-hidden="true">📍</span>
          <span>{{ local.endereco }}</span>
        </p>
        <p class="painel-detalhes__bairro">
          Bairro: <strong>{{ local.bairro }}</strong>
        </p>
      </div>

      <!-- Badge de classificação -->
      <div class="painel-detalhes__classificacao">
        <BadgeAcessibilidade
          :nivel="local.classificacao.nivel"
          :label="local.classificacao.label"
          :score="local.classificacao.score"
          :total="local.classificacao.total"
          :mostrarScore="true"
        />

        <div
          class="painel-detalhes__progresso"
          role="progressbar"
          :aria-valuenow="local.classificacao.score"
          :aria-valuemin="0"
          :aria-valuemax="local.classificacao.total"
          :aria-label="`Pontuação de acessibilidade: ${local.classificacao.score} de ${local.classificacao.total} recursos`"
        >
          <div
            class="painel-detalhes__progresso-barra"
            :class="`nivel-${local.classificacao.nivel}`"
            :style="{ width: `${(local.classificacao.score / local.classificacao.total) * 100}%` }"
          ></div>
        </div>
        <p class="painel-detalhes__progresso-texto" aria-hidden="true">
          {{ local.classificacao.score }} de {{ local.classificacao.total }} recursos disponíveis
        </p>
      </div>

      <!-- Descrição -->
      <p v-if="local.descricao" class="painel-detalhes__descricao">
        {{ local.descricao }}
      </p>

      <hr class="divider" />

      <!-- Recursos de acessibilidade -->
      <section aria-labelledby="recursos-heading">
        <h3 id="recursos-heading" class="painel-detalhes__recursos-titulo">
          Recursos de Acessibilidade
        </h3>

        <ul role="list" class="painel-detalhes__recursos-lista">
          <li
            v-for="(meta, chave) in RECURSOS_META"
            :key="chave"
            class="painel-detalhes__recurso"
            :class="{ 'is-disponivel': local.acessibilidade[chave] }"
          >
            <span class="painel-detalhes__recurso-icone" aria-hidden="true">
              {{ meta.icone }}
            </span>

            <span class="painel-detalhes__recurso-nome">{{ meta.label }}</span>

            <span
              class="painel-detalhes__recurso-status"
              :class="local.acessibilidade[chave] ? 'status-sim' : 'status-nao'"
              :aria-label="local.acessibilidade[chave] ? `${meta.label}: disponível` : `${meta.label}: não disponível`"
            >
              <span aria-hidden="true">
                {{ local.acessibilidade[chave] ? '✓' : '✗' }}
              </span>
              <span class="sr-only">
                {{ local.acessibilidade[chave] ? 'Disponível' : 'Não disponível' }}
              </span>
            </span>
          </li>
        </ul>
      </section>

      <hr class="divider" />

      <!-- ── AVALIAÇÕES DA COMUNIDADE ──────────────────────── -->
      <ListaComentarios
        :local-id="local.id"
        :limite="3"
      />

      <!-- Botão para avaliar este local -->
      <RouterLink
        :to="{ name: 'contribuir', query: { id: local.id } }"
        class="br-button secondary painel-detalhes__btn-contribuir"
        :aria-label="`Adicionar avaliação de acessibilidade para ${local.nome}`"
      >
        <span aria-hidden="true">✍️</span>
        Avaliar este local
      </RouterLink>

    </div>
  </aside>
</template>

<script setup>
import BadgeAcessibilidade from '@/components/BadgeAcessibilidade.vue'
import ListaComentarios from '@/components/ListaComentarios.vue'
import { RECURSOS_META } from '@/services/acessibilidadeService.js'

defineProps({
  local: { type: Object, default: null }
})

defineEmits(['fechar'])
</script>

<style scoped>
.painel-detalhes {
  width: var(--sidebar-width);
  min-width: var(--sidebar-width);
  background: var(--color-surface);
  border-left: 1px solid var(--color-gray-10);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  transition: width var(--transition-base);
}

.painel-detalhes__vazio {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-4);
  height: 100%;
  padding: var(--space-8);
  text-align: center;
  color: var(--color-text-secondary);
}
.painel-detalhes__vazio-icon { font-size: 3rem; }

.painel-detalhes__conteudo {
  padding: var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.painel-detalhes__header-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: var(--space-2);
}

.painel-detalhes__tipo-tag {
  display: inline-block;
  padding: var(--space-1) var(--space-3);
  background: var(--color-primary-lightest);
  color: var(--color-primary-dark);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  border-radius: var(--radius-full);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.painel-detalhes__fechar {
  color: var(--color-gray-60) !important;
  padding: var(--space-1) !important;
  min-height: unset !important;
}

.painel-detalhes__nome {
  font-size: var(--font-size-xl);
  color: var(--color-primary-dark);
  margin-bottom: var(--space-2);
}

.painel-detalhes__endereco {
  display: flex;
  gap: var(--space-2);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-1);
}
.painel-detalhes__bairro {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-bottom: 0;
}

.painel-detalhes__classificacao {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.painel-detalhes__progresso {
  height: 8px;
  background: var(--color-gray-10);
  border-radius: var(--radius-full);
  overflow: hidden;
}
.painel-detalhes__progresso-barra {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width var(--transition-slow);
}
.painel-detalhes__progresso-barra.nivel-total   { background: var(--color-accessible-green); }
.painel-detalhes__progresso-barra.nivel-parcial { background: var(--color-warning-dark); }
.painel-detalhes__progresso-barra.nivel-nao     { background: var(--color-accessible-red); }

.painel-detalhes__progresso-texto {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  margin-bottom: 0;
}

.painel-detalhes__descricao {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  line-height: var(--line-height-relaxed);
  background: var(--color-gray-05);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  border-left: 3px solid var(--color-primary-light);
  margin-bottom: 0;
}

.painel-detalhes__recursos-titulo {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-secondary);
  margin-bottom: var(--space-3);
}

.painel-detalhes__recursos-lista {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.painel-detalhes__recurso {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  border-radius: var(--radius-sm);
  background: var(--color-gray-05);
  opacity: 0.6;
  transition: opacity var(--transition-fast);
}
.painel-detalhes__recurso.is-disponivel {
  opacity: 1;
  background: var(--color-success-light);
}

.painel-detalhes__recurso-icone {
  font-size: 1.1rem;
  flex-shrink: 0;
  width: 24px;
  text-align: center;
}

.painel-detalhes__recurso-nome {
  flex: 1;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}

.painel-detalhes__recurso-status {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  flex-shrink: 0;
}
.status-sim { color: var(--color-accessible-green); }
.status-nao { color: var(--color-accessible-red); }

/* Botão contribuir */
.painel-detalhes__btn-contribuir {
  width: 100%;
  justify-content: center;
  margin-top: var(--space-2);
}

@media (max-width: 900px) {
  .painel-detalhes {
    width: 100%;
    min-width: unset;
    border-left: none;
    border-top: 1px solid var(--color-gray-10);
    max-height: 50vh;
  }
}
</style>