<template>
  <!--
    <section> com aria-labelledby aponta para o h2 do formulário.
    Isso cria uma landmark region nomeada para leitores de tela (WCAG 1.3.1).
  -->
  <section
    class="form-avaliacao br-card"
    aria-labelledby="form-avaliacao-titulo"
  >
    <div class="form-avaliacao__header">
      <h2 id="form-avaliacao-titulo" class="form-avaliacao__titulo">
        <Pencil aria-hidden="true" :size="20" />
        Registrar Avaliação
      </h2>
      <p class="form-avaliacao__subtitulo">
        Compartilhe sua experiência sobre a acessibilidade deste local.
        Sua contribuição ajuda outras pessoas com deficiência.
      </p>
    </div>

    <!--
      Não usamos <form> com action para evitar recarregamento de página.
      O role="form" + aria-labelledby garante semântica equivalente (WCAG 4.1.2).
    -->
    <div
      role="form"
      :aria-labelledby="'form-avaliacao-titulo'"
      class="form-avaliacao__corpo"
      @keydown.enter.prevent
    >

      <!-- ── 1. LOCAL SELECIONADO (readonly) ─────────────── -->
      <div v-if="local" class="form-avaliacao__local-info" role="group" aria-label="Local selecionado">
        <MapPin class="form-avaliacao__local-tag" aria-hidden="true" :size="20" />
        <div>
          <p class="form-avaliacao__local-nome">{{ local.nome }}</p>
          <p class="form-avaliacao__local-end">{{ local.endereco }} — {{ local.bairro }}</p>
        </div>
      </div>

      <!-- ── 2. PERGUNTA PRINCIPAL: ACESSÍVEL? ────────────── -->
      <!--
        fieldset + legend é o padrão semântico correto para grupos
        de radio buttons (WCAG 1.3.1, H71).
      -->
      <fieldset class="form-avaliacao__fieldset" :class="{ 'has-error': erros.acessivel }">
        <legend class="form-avaliacao__legend">
          Este local é acessível?
          <span class="form-avaliacao__obrigatorio" aria-label="campo obrigatório">*</span>
        </legend>

        <div class="form-avaliacao__radios">

          <!-- Radio: Sim ─────────────────────────────────── -->
          <label
            class="br-radio form-avaliacao__radio-label"
            :class="{ 'is-selected': avaliacaoLocal === true }"
            for="radio-sim"
          >
            <input
              id="radio-sim"
              v-model="avaliacaoLocal"
              type="radio"
              name="acessivel"
              :value="true"
              aria-describedby="radio-sim-desc"
              @change="erros.acessivel = ''"
            />
            <CheckCircle class="form-avaliacao__radio-icon" aria-hidden="true" :size="20" style="color: var(--color-accessible-green);" />
            <span class="form-avaliacao__radio-texto">
              Sim, é acessível
            </span>
            <span id="radio-sim-desc" class="sr-only">
              O local possui recursos adequados de acessibilidade
            </span>
          </label>

          <!-- Radio: Não ─────────────────────────────────── -->
          <label
            class="br-radio form-avaliacao__radio-label"
            :class="{ 'is-selected': avaliacaoLocal === false }"
            for="radio-nao"
          >
            <input
              id="radio-nao"
              v-model="avaliacaoLocal"
              type="radio"
              name="acessivel"
              :value="false"
              aria-describedby="radio-nao-desc"
              @change="erros.acessivel = ''"
            />
            <XCircle class="form-avaliacao__radio-icon" aria-hidden="true" :size="20" style="color: var(--color-accessible-red);" />
            <span class="form-avaliacao__radio-texto">
              Não, há barreiras
            </span>
            <span id="radio-nao-desc" class="sr-only">
              O local apresenta barreiras ou dificuldades de acessibilidade
            </span>
          </label>

        </div>

        <!-- Mensagem de erro inline (WCAG 3.3.1) -->
        <p
          v-if="erros.acessivel"
          id="erro-acessivel"
          role="alert"
          class="form-avaliacao__erro"
          aria-live="polite"
        >
          <TriangleAlert aria-hidden="true" :size="16" />
           {{ erros.acessivel }}
        </p>
      </fieldset>

      <!-- ── 3. COMENTÁRIO ───────────────────────────────── -->
      <div class="form-avaliacao__campo" :class="{ 'has-error': erros.comentario }">
        <label
          for="comentario-input"
          class="form-avaliacao__label"
        >
          Conte sua experiência
          <span class="form-avaliacao__obrigatorio" aria-label="campo obrigatório">*</span>
        </label>
        <p id="comentario-instrucao" class="form-avaliacao__instrucao">
          Descreva o que observou sobre a acessibilidade. Ex.: presença de rampas,
          estado das calçadas, funcionamento de elevadores, etc.
          (mínimo 10, máximo 500 caracteres)
        </p>

        <div class="form-avaliacao__textarea-wrapper">
          <textarea
            id="comentario-input"
            v-model="comentario"
            class="br-textarea"
            rows="4"
            maxlength="500"
            placeholder="Ex.: O local possui rampa de acesso ampla, mas o banheiro adaptado estava bloqueado com caixas..."
            :aria-describedby="`comentario-instrucao${erros.comentario ? ' erro-comentario' : ''}`"
            :aria-invalid="!!erros.comentario"
            @input="erros.comentario = ''"
          ></textarea>

          <!-- Contador de caracteres (WCAG 3.3.2) -->
          <div
            class="form-avaliacao__contador"
            :class="{ 'is-limite': comentario.length > 450 }"
            aria-live="polite"
            aria-atomic="true"
          >
            <span class="sr-only">Caracteres digitados: </span>
            {{ comentario.length }}/500
          </div>
        </div>

        <p
          v-if="erros.comentario"
          id="erro-comentario"
          role="alert"
          class="form-avaliacao__erro"
          aria-live="polite"
        >
          <span aria-hidden="true">⚠</span> {{ erros.comentario }}
        </p>
      </div>

      <!-- ── 4. USUÁRIO AUTENTICADO ─────────────────────────── -->
      <div class="form-avaliacao__usuario-info" aria-label="Enviando como">
        <User aria-hidden="true" :size="20" />
        <div>
          <p class="form-avaliacao__usuario-label">Enviando como</p>
          <p class="form-avaliacao__usuario-nome">{{ nomeAutor }}</p>
        </div>
      </div>

      <!-- ── 5. AÇÕES ────────────────────────────────────── -->
      <div class="form-avaliacao__acoes">
        <button
          type="button"
          class="br-button primary form-avaliacao__submit"
          :disabled="enviando"
          :aria-busy="enviando"
          aria-describedby="submit-desc"
          @click="submeter"
        >
          <Loader2 v-if="enviando" aria-hidden="true" class="form-avaliacao__spinner" :size="20" style="margin-right: 6px;" />
          <Send v-else aria-hidden="true" :size="20" style="margin-right: 6px;" />
          {{ enviando ? 'Enviando...' : 'Enviar contribuição' }}
        </button>
        <span id="submit-desc" class="sr-only">
          Envia sua avaliação de acessibilidade para o local selecionado
        </span>

        <button
          type="button"
          class="br-button secondary"
          @click="limpar"
          :disabled="enviando"
        >
          Limpar
        </button>
      </div>

      <!-- ── 6. FEEDBACK DE SUCESSO (WCAG 4.1.3) ────────── -->
      <div
        v-if="sucesso"
        role="alert"
        aria-live="assertive"
        class="form-avaliacao__sucesso"
      >
        <PartyPopper aria-hidden="true" class="form-avaliacao__sucesso-icone" :size="24" />
        <div>
          <p class="form-avaliacao__sucesso-titulo">Contribuição enviada!</p>
          <p class="form-avaliacao__sucesso-msg">
            Obrigado por ajudar a tornar Teresina mais acessível para todos.
          </p>
        </div>
      </div>

    </div>
  </section>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { enviarAvaliacao } from '@/services/avaliacoesService.js'
import { useAuth } from '@/services/authService.js'
import { Pencil, MapPin, CheckCircle, XCircle, TriangleAlert, User, Loader2, Send, PartyPopper } from 'lucide-vue-next'

const props = defineProps({
  local: { type: Object, default: null }
})

const emit = defineEmits(['enviado'])

const { usuarioAtual } = useAuth()

// Nome exibido: usa o do usuário logado ou "Cidadão Anônimo"
const nomeAutor = computed(() => usuarioAtual.value?.nome || 'Cidadão Anônimo')

// ── Estado do formulário ──────────────────────────────────────
const avaliacaoLocal = ref(null)
const comentario     = ref('')
const enviando       = ref(false)
const sucesso        = ref(false)

const erros = reactive({
  acessivel:  '',
  comentario: ''
})

// ── Validação ─────────────────────────────────────────────────
function validar() {
  let valido = true

  if (avaliacaoLocal.value === null) {
    erros.acessivel = 'Por favor, informe se o local é acessível ou não.'
    valido = false
  }

  if (comentario.value.trim().length < 10) {
    erros.comentario = 'O comentário deve ter ao menos 10 caracteres.'
    valido = false
  }

  return valido
}

// ── Submissão ─────────────────────────────────────────────────
async function submeter() {
  sucesso.value = false
  if (!props.local) return
  if (!validar()) return

  enviando.value = true

  try {
    await new Promise(r => setTimeout(r, 600))

    // Passa o nome do usuário autenticado automaticamente
    const resultado = await enviarAvaliacao(
      props.local.id,
      avaliacaoLocal.value,
      comentario.value
    )

    sucesso.value = true
    emit('enviado', resultado.avaliacao)
    limpar(true)

  } catch (err) {
    erros.comentario = err.message
  } finally {
    enviando.value = false
  }
}

// ── Limpar formulário ─────────────────────────────────────────
function limpar(manterSucesso = false) {
  avaliacaoLocal.value = null
  comentario.value     = ''
  autor.value          = ''
  erros.acessivel      = ''
  erros.comentario     = ''
  if (!manterSucesso) sucesso.value = false
}
</script>

<style scoped>
/* ── CARD WRAPPER ──────────────────────────────────────────── */
.form-avaliacao {
  padding: var(--space-6);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-gray-10);
  background: var(--color-surface);
  box-shadow: var(--shadow-sm);
}

/* ── HEADER ────────────────────────────────────────────────── */
.form-avaliacao__header {
  margin-bottom: var(--space-6);
  padding-bottom: var(--space-4);
  border-bottom: 2px solid var(--color-primary-lightest);
}
.form-avaliacao__titulo {
  font-size: var(--font-size-xl);
  color: var(--color-primary-dark);
  margin-bottom: var(--space-2);
  display: flex;
  align-items: center;
  gap: var(--space-2);
}
.form-avaliacao__subtitulo {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-bottom: 0;
  line-height: var(--line-height-relaxed);
}

/* ── CORPO ─────────────────────────────────────────────────── */
.form-avaliacao__corpo {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

/* ── LOCAL INFO ────────────────────────────────────────────── */
.form-avaliacao__local-info {
  display: flex;
  gap: var(--space-3);
  align-items: flex-start;
  background: var(--color-primary-lightest);
  border: 1px solid var(--color-primary-light);
  border-radius: var(--radius-md);
  padding: var(--space-4);
}
.form-avaliacao__local-tag { font-size: 1.25rem; flex-shrink: 0; }
.form-avaliacao__local-nome {
  font-weight: var(--font-weight-bold);
  color: var(--color-primary-dark);
  margin-bottom: var(--space-1);
}
.form-avaliacao__local-end {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-bottom: 0;
}

/* ── FIELDSET RADIO ────────────────────────────────────────── */
.form-avaliacao__fieldset {
  border: 1px solid var(--color-gray-20);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  transition: border-color var(--transition-fast);
}
.form-avaliacao__fieldset.has-error { border-color: var(--color-danger); }

.form-avaliacao__legend {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  padding: 0 var(--space-2);
}

.form-avaliacao__radios {
  display: flex;
  gap: var(--space-4);
  margin-top: var(--space-4);
  flex-wrap: wrap;
}

/* Card-style radio (visual melhorado sem perder semântica) */
.form-avaliacao__radio-label {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex: 1;
  min-width: 160px;
  padding: var(--space-4);
  border: 2px solid var(--color-gray-20);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: border-color var(--transition-fast), background var(--transition-fast);
  background: var(--color-white);
}
.form-avaliacao__radio-label:hover {
  border-color: var(--color-primary-default);
  background: var(--color-primary-lightest);
}
.form-avaliacao__radio-label.is-selected {
  border-color: var(--color-primary-default);
  background: var(--color-primary-lightest);
  box-shadow: 0 0 0 2px var(--color-primary-default);
}
.form-avaliacao__radio-label input[type="radio"] {
  accent-color: var(--color-primary-default);
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}
.form-avaliacao__radio-icon { font-size: 1.25rem; }
.form-avaliacao__radio-texto {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
}

/* ── CAMPOS ────────────────────────────────────────────────── */
.form-avaliacao__campo {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}
.form-avaliacao__campo.has-error .br-textarea,
.form-avaliacao__campo.has-error .br-input {
  border-color: var(--color-danger);
  box-shadow: 0 0 0 2px rgba(229, 34, 7, .2);
}

.form-avaliacao__label {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
}
.form-avaliacao__obrigatorio {
  color: var(--color-danger);
  font-weight: var(--font-weight-bold);
  margin-left: var(--space-1);
}
.form-avaliacao__opcional {
  font-weight: var(--font-weight-regular);
  color: var(--color-text-secondary);
  font-size: var(--font-size-xs);
  margin-left: var(--space-1);
}
.form-avaliacao__instrucao {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  margin-bottom: 0;
  line-height: var(--line-height-relaxed);
}

/* Textarea gov.br */
.br-textarea {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  font-family: var(--font-family-base);
  font-size: var(--font-size-md);
  color: var(--color-text-primary);
  background: var(--color-white);
  border: 1px solid var(--color-gray-40);
  border-radius: var(--radius-md);
  resize: vertical;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
  min-height: 110px;
  line-height: var(--line-height-relaxed);
}
.br-textarea:focus {
  outline: none;
  border-color: var(--color-primary-default);
  box-shadow: 0 0 0 3px rgba(19, 81, 180, .25);
}
.br-textarea::placeholder { color: var(--color-gray-40); }

/* Wrapper para textarea + contador */
.form-avaliacao__textarea-wrapper { position: relative; }
.form-avaliacao__contador {
  text-align: right;
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  margin-top: var(--space-1);
  transition: color var(--transition-fast);
}
.form-avaliacao__contador.is-limite { color: var(--color-warning-dark); font-weight: var(--font-weight-semibold); }

/* ── ERRO INLINE ───────────────────────────────────────────── */
.form-avaliacao__erro {
  font-size: var(--font-size-sm);
  color: var(--color-danger);
  font-weight: var(--font-weight-medium);
  display: flex;
  align-items: center;
  gap: var(--space-1);
  margin-bottom: 0;
}

/* ── AÇÕES ─────────────────────────────────────────────────── */
.form-avaliacao__acoes {
  display: flex;
  gap: var(--space-3);
  flex-wrap: wrap;
}
.form-avaliacao__submit { min-width: 200px; }
.form-avaliacao__spinner {
  display: inline-block;
  animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── SUCESSO ───────────────────────────────────────────────── */
.form-avaliacao__sucesso {
  display: flex;
  align-items: flex-start;
  gap: var(--space-4);
  padding: var(--space-4) var(--space-5);
  background: var(--color-success-light);
  border: 1px solid var(--color-accessible-green);
  border-radius: var(--radius-md);
  border-left: 4px solid var(--color-accessible-green);
}
.form-avaliacao__sucesso-icone { font-size: 1.5rem; flex-shrink: 0; }
.form-avaliacao__sucesso-titulo {
  font-weight: var(--font-weight-bold);
  color: var(--color-accessible-green);
  margin-bottom: var(--space-1);
}
.form-avaliacao__sucesso-msg {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-bottom: 0;
}

/* ── RESPONSIVO ────────────────────────────────────────────── */
@media (max-width: 500px) {
  .form-avaliacao__radios { flex-direction: column; }
  .form-avaliacao__acoes  { flex-direction: column; }
  .form-avaliacao__submit { min-width: unset; width: 100%; }
}

/* ── USUÁRIO AUTENTICADO ─────────────────────────────────────── */
.form-avaliacao__usuario-info {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background: var(--color-primary-lightest);
  border: 1px solid var(--color-primary-light);
  border-radius: var(--radius-md);
  font-size: 1.25rem;
}
.form-avaliacao__usuario-label {
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  margin-bottom: 2px;
}
.form-avaliacao__usuario-nome {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-bold);
  color: var(--color-primary-dark);
  margin-bottom: 0;
}
</style>