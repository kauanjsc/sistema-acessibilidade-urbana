/**
 * authService.js
 * Suporta dois modos controlados por VITE_USE_MOCK:
 *   true  → autenticação simulada com usuarios.json (sem backend)
 *   false → autenticação real via API FastAPI com JWT
 */

import { ref, computed } from 'vue'
import { api } from './apiClient.js'
import usuariosData from '@/data/usuarios.json'

const USE_MOCK   = import.meta.env.VITE_USE_MOCK === 'true'
const STORAGE_KEY = 'teresina_acessivel_user'

// ── Estado reativo global (singleton) ────────────────────────
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
// LOGIN
// ─────────────────────────────────────────────────────────────
export async function login(email, senha) {
  if (!email || !senha) {
    return { sucesso: false, erro: 'Preencha todos os campos.' }
  }

  // ── MOCK ──────────────────────────────────────────────────
  if (USE_MOCK) {
    const usuario = usuariosData.find(
      u => u.email.toLowerCase() === email.toLowerCase().trim()
        && u.senha === senha
    )
    if (!usuario) {
      return { sucesso: false, erro: 'E-mail ou senha incorretos.' }
    }
    const sessao = {
      id:     usuario.id,
      nome:   usuario.nome,
      email:  usuario.email,
      perfil: usuario.perfil,
      avatar: usuario.avatar,
      token:  'mock-token',
    }
    _usuarioAtual.value = sessao
    localStorage.setItem(STORAGE_KEY, JSON.stringify(sessao))
    return { sucesso: true, usuario: sessao }
  }

  // ── API REAL ───────────────────────────────────────────────
  try {
    const data = await api.post('/auth/login', { email, senha })
    // data = { access_token, token_type, usuario }
    const sessao = {
      id:     data.usuario.id,
      nome:   data.usuario.nome,
      email:  data.usuario.email,
      perfil: data.usuario.perfil,
      token:  data.access_token,
    }
    _usuarioAtual.value = sessao
    localStorage.setItem(STORAGE_KEY, JSON.stringify(sessao))
    return { sucesso: true, usuario: sessao }
  } catch (err) {
    return { sucesso: false, erro: err.message }
  }
}

// ─────────────────────────────────────────────────────────────
// LOGOUT / GETTERS
// ─────────────────────────────────────────────────────────────
export function logout() {
  _usuarioAtual.value = null
  localStorage.removeItem(STORAGE_KEY)
}

export function getUser()         { return _usuarioAtual.value }
export function isAuthenticated() { return _usuarioAtual.value !== null }

export const usuarioAtual = computed(() => _usuarioAtual.value)
export const autenticado  = computed(() => _usuarioAtual.value !== null)

export function useAuth() {
  return {
    usuarioAtual,
    autenticado,
    login,
    logout,
    getUser,
    isAuthenticated,
  }
}