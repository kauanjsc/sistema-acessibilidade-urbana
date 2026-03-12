/**
 * authService.js
 * Serviço de autenticação simulada para o protótipo Teresina Acessível.
 *
 * Em produção, as funções login/logout fariam chamadas a uma API REST.
 * Aqui simulamos com usuarios.json e persistimos a sessão no localStorage.
 */

import { ref, computed } from 'vue'
import usuariosData from '@/data/usuarios.json'

// ── Chave usada no localStorage ───────────────────────────────
const STORAGE_KEY = 'teresina_acessivel_user'

// ── Estado reativo global (singleton) ────────────────────────
// Inicializa a partir do localStorage para persistir entre recarregamentos
const _usuarioAtual = ref(carregarSessao())

function carregarSessao() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

// ─────────────────────────────────────────────────────────────
// FUNÇÕES PÚBLICAS
// ─────────────────────────────────────────────────────────────

/**
 * Realiza o login com email e senha.
 * Compara com os usuários do mock e salva sessão no localStorage.
 *
 * @param {string} email
 * @param {string} senha
 * @returns {{ sucesso: boolean, erro?: string, usuario?: Object }}
 */
export function login(email, senha) {
  if (!email || !senha) {
    return { sucesso: false, erro: 'Preencha todos os campos.' }
  }

  const usuario = usuariosData.find(
    u => u.email.toLowerCase() === email.toLowerCase().trim() && u.senha === senha
  )

  if (!usuario) {
    return { sucesso: false, erro: 'E-mail ou senha incorretos.' }
  }

  // Nunca salvar a senha na sessão
  const sessao = {
    id:     usuario.id,
    nome:   usuario.nome,
    email:  usuario.email,
    perfil: usuario.perfil,
    avatar: usuario.avatar
  }

  _usuarioAtual.value = sessao
  localStorage.setItem(STORAGE_KEY, JSON.stringify(sessao))

  return { sucesso: true, usuario: sessao }
}

/**
 * Encerra a sessão do usuário.
 */
export function logout() {
  _usuarioAtual.value = null
  localStorage.removeItem(STORAGE_KEY)
}

/**
 * Retorna os dados do usuário logado (ou null).
 * @returns {Object|null}
 */
export function getUser() {
  return _usuarioAtual.value
}

/**
 * Verifica se há um usuário autenticado.
 * @returns {boolean}
 */
export function isAuthenticated() {
  return _usuarioAtual.value !== null
}

// ── Exporta ref reativa para uso em componentes Vue ──────────
// Componentes podem fazer: const { usuarioAtual } = useAuth()
export const usuarioAtual = computed(() => _usuarioAtual.value)
export const autenticado  = computed(() => _usuarioAtual.value !== null)

/**
 * Composable para usar auth em componentes Vue.
 * Uso: const { usuarioAtual, autenticado, login, logout } = useAuth()
 */
export function useAuth() {
  return {
    usuarioAtual,
    autenticado,
    login,
    logout,
    getUser,
    isAuthenticated
  }
}