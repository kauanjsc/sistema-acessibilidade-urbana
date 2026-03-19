/**
 * apiClient.js
 * Cliente HTTP central da aplicação.
 * - Define a BASE_URL da API
 * - Injeta o token JWT no header Authorization automaticamente
 * - Trata erros HTTP de forma padronizada
 */

const BASE_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, '')

function getToken() {
  try {
    const raw = localStorage.getItem('teresina_acessivel_user')
    if (!raw) return null
    const sessao = JSON.parse(raw)
    return sessao?.token || null
  } catch {
    return null
  }
}

function buildUrl(path) {
  if (!path) return BASE_URL
  return path.startsWith('/') ? `${BASE_URL}${path}` : `${BASE_URL}/${path}`
}

async function request(path, options = {}) {
  const token = getToken()

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  }

  if (token) headers.Authorization = `Bearer ${token}`

  const payload = { ...options, headers }
  if (payload.body !== undefined && typeof payload.body !== 'string') {
    payload.body = JSON.stringify(payload.body)
  }

  const response = await fetch(buildUrl(path), payload)

  // Trata erro 401 — token expirado ou inválido
  if (response.status === 401) {
    localStorage.removeItem('teresina_acessivel_user')
    window.location.href = '/login'
    throw new Error('Sessão expirada. Faça login novamente.')
  }

  if (!response.ok) {
    const text = await response.text().catch(() => '')
    const erro = text ? JSON.parse(text) : {}
    throw new Error(erro.detail || `Erro ${response.status}`)
  }

  if (response.status === 204) return null

  const text = await response.text().catch(() => '')
  if (!text) return null
  return JSON.parse(text)
}

export const api = {
  get:    (path)       => request(path, { method: 'GET' }),
  post:   (path, body) => request(path, { method: 'POST', body }),
  put:    (path, body) => request(path, { method: 'PUT',  body }),
  delete: (path)       => request(path, { method: 'DELETE' }),
}