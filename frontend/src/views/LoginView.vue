<template>
  <div class="login-page">

    <!-- Faixa gov.br decorativa -->
    <div class="login-page__govbr-bar" aria-hidden="true">
      <span>🇧🇷 gov.br</span>
    </div>

    <main class="login-page__main" id="main-content">
      <div class="login-page__container">

        <!-- Logo / identidade -->
        <div class="login-page__brand" aria-label="Teresina Acessível">
          <span class="login-page__brand-icon" aria-hidden="true">♿</span>
          <div>
            <p class="login-page__brand-name">Teresina Acessível</p>
            <p class="login-page__brand-sub">Mapeamento de Acessibilidade Urbana</p>
          </div>
        </div>

        <!-- Card de login -->
        <div class="br-card login-card" role="main">

          <div class="login-card__header">
            <h1 class="login-card__titulo">Entrar na plataforma</h1>
            <p class="login-card__subtitulo">
              Acesse com seu e-mail e senha para registrar contribuições.
            </p>
          </div>

          <!-- Alerta de erro geral -->
          <div
            v-if="erroGeral"
            role="alert"
            aria-live="assertive"
            class="login-card__alerta"
          >
            <span aria-hidden="true">⚠</span>
            {{ erroGeral }}
          </div>

          <!-- Formulário -->
          <div
            role="form"
            aria-labelledby="login-titulo"
            class="login-card__form"
          >

            <!-- E-mail -->
            <div class="login-campo" :class="{ 'has-error': erros.email }">
              <label for="login-email" class="login-campo__label">
                E-mail
                <span class="login-campo__obrigatorio" aria-label="obrigatório">*</span>
              </label>
              <input
                id="login-email"
                v-model="email"
                type="email"
                class="br-input"
                placeholder="seu@email.com"
                autocomplete="email"
                :aria-invalid="!!erros.email"
                :aria-describedby="erros.email ? 'erro-email' : undefined"
                @input="erros.email = ''; erroGeral = ''"
                @keydown.enter="submeter"
              />
              <p v-if="erros.email" id="erro-email" role="alert" class="login-campo__erro">
                <span aria-hidden="true">⚠</span> {{ erros.email }}
              </p>
            </div>

            <!-- Senha -->
            <div class="login-campo" :class="{ 'has-error': erros.senha }">
              <label for="login-senha" class="login-campo__label">
                Senha
                <span class="login-campo__obrigatorio" aria-label="obrigatório">*</span>
              </label>
              <div class="login-campo__senha-wrapper">
                <input
                  id="login-senha"
                  v-model="senha"
                  :type="mostrarSenha ? 'text' : 'password'"
                  class="br-input"
                  placeholder="Sua senha"
                  autocomplete="current-password"
                  :aria-invalid="!!erros.senha"
                  :aria-describedby="erros.senha ? 'erro-senha' : undefined"
                  @input="erros.senha = ''; erroGeral = ''"
                  @keydown.enter="submeter"
                />
                <button
                  type="button"
                  class="login-campo__toggle-senha"
                  :aria-label="mostrarSenha ? 'Ocultar senha' : 'Mostrar senha'"
                  @click="mostrarSenha = !mostrarSenha"
                >
                  {{ mostrarSenha ? '🙈' : '👁️' }}
                </button>
              </div>
              <p v-if="erros.senha" id="erro-senha" role="alert" class="login-campo__erro">
                <span aria-hidden="true">⚠</span> {{ erros.senha }}
              </p>
            </div>

            <!-- Botão entrar -->
            <button
              type="button"
              class="br-button primary login-card__btn-entrar"
              :disabled="carregando"
              :aria-busy="carregando"
              @click="submeter"
            >
              <span v-if="carregando" class="login-card__spinner" aria-hidden="true">⟳</span>
              <span aria-hidden="true" v-else>🔓</span>
              {{ carregando ? 'Entrando...' : 'Entrar' }}
            </button>

          </div>

          <!-- Dica de acesso (apenas em dev/protótipo) -->
          <details class="login-card__dica">
            <summary class="login-card__dica-summary">
              <span aria-hidden="true">💡</span> Ver credenciais de teste
            </summary>
            <div class="login-card__dica-corpo">
              <p class="login-card__dica-titulo">Usuários disponíveis no protótipo:</p>
              <ul class="login-card__dica-lista">
                <li v-for="u in usuariosDica" :key="u.email">
                  <button
                    type="button"
                    class="login-card__dica-btn"
                    :aria-label="`Preencher credenciais de ${u.nome}`"
                    @click="preencherDica(u)"
                  >
                    <span class="login-card__dica-avatar" aria-hidden="true">{{ u.avatar }}</span>
                    <span>
                      <strong>{{ u.nome }}</strong>
                      <small>{{ u.email }} · {{ u.senha }}</small>
                    </span>
                  </button>
                </li>
              </ul>
            </div>
          </details>

        </div>

        <!-- Link voltar -->
        <div class="login-page__voltar">
          <RouterLink to="/" class="login-page__voltar-link">
            ← Voltar para o início sem entrar
          </RouterLink>
        </div>

      </div>
    </main>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { login } from '@/services/authService.js'
import usuariosData from '@/data/usuarios.json'

const router = useRouter()
const route  = useRoute()

//  Estado ---------
const email       = ref('')
const senha       = ref('')
const mostrarSenha = ref(false)
const carregando  = ref(false)
const erroGeral   = ref('')
const erros = ref({ email: '', senha: '' })

// Dica de credenciais (sem a senha real exposta no DOM para admin)
const usuariosDica = usuariosData.map(u => ({
  nome:   u.nome,
  email:  u.email,
  senha:  u.senha,
  avatar: u.avatar
}))

//  Validação ------
function validar() {
  let valido = true
  erros.value = { email: '', senha: '' }

  if (!email.value.trim()) {
    erros.value.email = 'Informe seu e-mail.'
    valido = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
    erros.value.email = 'Informe um e-mail válido.'
    valido = false
  }

  if (!senha.value) {
    erros.value.senha = 'Informe sua senha.'
    valido = false
  }

  return valido
}

// Submissão --------
async function submeter() {
  erroGeral.value = ''
  if (!validar()) return

  carregando.value = true

  try {
    // 1. Chama o login real (que agora busca no Render)
    const resultado = await login(email.value.trim(), senha.value)

    if (resultado.sucesso) {
      // Se veio de uma página protegida, volta pra lá, senão vai para /contribuir
      const destino = route.query.redirect || '/contribuir'
      router.push(destino)
    } else {
      // 3.  ERRO: Mostra a mensagem do backend 
      erroGeral.value = resultado.erro || 'Falha na autenticação.'
    }
  } catch (err) {
    erroGeral.value = 'Erro de conexão com o servidor.'
  } finally {
    carregando.value = false
  }
}

//  Preencher dica 
function preencherDica(u) {
  email.value = u.email
  senha.value = u.senha
  erros.value = { email: '', senha: '' }
  erroGeral.value = ''
}
</script>

<style scoped>
/*  PÁGINA  */
.login-page {
  min-height: 100vh;
  background: linear-gradient(145deg, var(--color-primary-darker) 0%, var(--color-primary-dark) 50%, var(--color-primary-default) 100%);
  display: flex;
  flex-direction: column;
}

.login-page__govbr-bar {
  background: var(--color-primary-darker);
  color: rgba(255,255,255,.7);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  padding: var(--space-2) var(--space-6);
  border-bottom: 1px solid rgba(255,255,255,.1);
  letter-spacing: 0.05em;
}

.login-page__main {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-8) var(--space-4);
}

.login-page__container {
  width: 100%;
  max-width: 440px;
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

/*  BRAND  */
.login-page__brand {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  color: var(--color-white);
}
.login-page__brand-icon { font-size: 2.5rem; }
.login-page__brand-name {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-extrabold);
  line-height: 1;
  margin-bottom: var(--space-1);
}
.login-page__brand-sub {
  font-size: var(--font-size-xs);
  opacity: .75;
  margin-bottom: 0;
}

/*  CARD  */
.login-card {
  background: var(--color-white);
  border-radius: var(--radius-lg);
  padding: var(--space-8);
  box-shadow: 0 20px 60px rgba(0,0,0,.3);
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.login-card__header { display: flex; flex-direction: column; gap: var(--space-2); }
.login-card__titulo {
  font-size: var(--font-size-xl);
  color: var(--color-primary-dark);
  font-weight: var(--font-weight-extrabold);
}
.login-card__subtitulo {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-bottom: 0;
  line-height: var(--line-height-relaxed);
}

/*  ALERTA  */
.login-card__alerta {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background: var(--color-danger-light);
  border: 1px solid var(--color-accessible-red);
  border-left: 4px solid var(--color-accessible-red);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-accessible-red);
}

/*  FORM  */
.login-card__form { display: flex; flex-direction: column; gap: var(--space-5); }

.login-campo { display: flex; flex-direction: column; gap: var(--space-2); }
.login-campo__label {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
}
.login-campo__obrigatorio { color: var(--color-danger); margin-left: 2px; }
.login-campo__erro {
  font-size: var(--font-size-sm);
  color: var(--color-danger);
  display: flex;
  align-items: center;
  gap: var(--space-1);
  margin-bottom: 0;
}
.login-campo.has-error .br-input {
  border-color: var(--color-danger);
  box-shadow: 0 0 0 2px rgba(229,34,7,.15);
}

.login-campo__senha-wrapper { position: relative; }
.login-campo__senha-wrapper .br-input { padding-right: 3rem; }
.login-campo__toggle-senha {
  position: absolute;
  right: var(--space-3);
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  padding: var(--space-1);
  border-radius: var(--radius-sm);
  color: var(--color-text-secondary);
  min-height: 36px;
  min-width: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.login-campo__toggle-senha:focus-visible {
  outline: 3px solid var(--color-focus);
  outline-offset: 2px;
}

.login-card__btn-entrar {
  width: 100%;
  justify-content: center;
  font-size: var(--font-size-md);
  height: 48px;
}
.login-card__spinner {
  display: inline-block;
  animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/*  DICA  */
.login-card__dica {
  border-top: 1px solid var(--color-gray-10);
  padding-top: var(--space-4);
}
.login-card__dica-summary {
  cursor: pointer;
  font-size: var(--font-size-sm);
  color: var(--color-primary-default);
  font-weight: var(--font-weight-semibold);
  user-select: none;
  list-style: none;
  display: flex;
  align-items: center;
  gap: var(--space-2);
}
.login-card__dica-summary::-webkit-details-marker { display: none; }
.login-card__dica-summary:focus-visible {
  outline: 3px solid var(--color-focus);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}
.login-card__dica-corpo {
  margin-top: var(--space-3);
  padding: var(--space-4);
  background: var(--color-gray-05);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-gray-10);
}
.login-card__dica-titulo {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: var(--space-3);
}
.login-card__dica-lista { list-style: none; display: flex; flex-direction: column; gap: var(--space-2); }
.login-card__dica-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: var(--space-3);
  background: var(--color-white);
  border: 1px solid var(--color-gray-20);
  border-radius: var(--radius-md);
  padding: var(--space-3) var(--space-4);
  cursor: pointer;
  text-align: left;
  transition: border-color var(--transition-fast), background var(--transition-fast);
  min-height: 44px;
}
.login-card__dica-btn:hover {
  border-color: var(--color-primary-default);
  background: var(--color-primary-lightest);
}
.login-card__dica-btn:focus-visible {
  outline: 3px solid var(--color-focus);
  outline-offset: 2px;
}
.login-card__dica-avatar {
  width: 36px; height: 36px;
  background: var(--color-primary-default);
  color: var(--color-white);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-bold);
  flex-shrink: 0;
}
.login-card__dica-btn strong {
  display: block;
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
}
.login-card__dica-btn small {
  display: block;
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  margin-top: 2px;
}

/*  VOLTAR  */
.login-page__voltar { text-align: center; }
.login-page__voltar-link {
  color: rgba(255,255,255,.8);
  font-size: var(--font-size-sm);
  text-decoration: none;
  transition: color var(--transition-fast);
}
.login-page__voltar-link:hover { color: var(--color-white); }
.login-page__voltar-link:focus-visible {
  outline: 3px solid var(--color-focus);
  outline-offset: 4px;
  border-radius: var(--radius-sm);
}
</style>