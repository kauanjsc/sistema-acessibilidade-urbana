/**
 * acessibilidadeService.js
 * Suporta dois modos controlados por VITE_USE_MOCK:
 *   true  → carrega locais.json local (sem backend)
 *   false → busca da API real GET /locais
 */

import { api } from './apiClient.js'
import locaisData from '@/data/locais.json'
import { 
  ShoppingBag, Hospital, GraduationCap, TreePine, Building2, Landmark, 
  Store, Theater, BusFront, ShoppingCart, Trophy,
  Accessibility, Users, CircleParking, ArrowUpCircle, DoorOpen, Footprints
} from 'lucide-vue-next'

const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'

// ── Enriquece local com campo classificacao ───────────────────
// O MapaInterativo.vue e FiltroAcessibilidade esperam local.classificacao.nivel
// Valores: 'total' | 'parcial' | 'nao'  (alinhados com FiltroAcessibilidade.vue)
function enriquecerLocal(local) {
  const nivel = classificarAcessibilidade(local)
  const mapa = {
    alto:  { nivel: 'total',   label: 'Totalmente Acessível'    },
    medio: { nivel: 'parcial', label: 'Parcialmente Acessível'  },
    baixo: { nivel: 'nao',     label: 'Não Acessível'           },
  }
  const { nivel: nivelMapeado, label } = mapa[nivel] || mapa.baixo
  return {
    ...local,
    classificacao: { nivel: nivelMapeado, label }
  }
}

// ── Buscar todos os locais ────────────────────────────────────
export async function getLocais() {
  if (USE_MOCK) return locaisData.map(enriquecerLocal)
  const locais = await api.get('/locais')
  return locais.map(enriquecerLocal)
}

// ── Buscar local por ID ───────────────────────────────────────
export async function getLocalById(id) {
  if (USE_MOCK) {
    const local = locaisData.find(l => l.id === Number(id)) || null
    return local ? enriquecerLocal(local) : null
  }
  const local = await api.get(`/locais/${id}`)
  return enriquecerLocal(local)
}

// ── Filtros (sempre no frontend) ──────────────────────────────
export function filtrarPorBusca(locais, termo) {
  const t = termo.toLowerCase().trim()
  if (!t) return locais
  return locais.filter(l =>
    l.nome.toLowerCase().includes(t) ||
    l.bairro.toLowerCase().includes(t) ||
    l.endereco.toLowerCase().includes(t)
  )
}

// recursos = objeto ex: { rampa: true, elevador: true }
export function filtrarPorAcessibilidade(locais, recursos) {
  const recursosAtivos = Object.keys(recursos).filter(k => recursos[k])
  if (recursosAtivos.length === 0) return locais
  return locais.filter(l =>
    recursosAtivos.every(recurso => l.acessibilidade?.[recurso] === true)
  )
}

// niveis = array de strings ex: ['total', 'parcial']
export function filtrarPorNivel(locais, niveis) {
  if (!niveis || niveis.length === 0) return locais
  return locais.filter(l => niveis.includes(l.classificacao?.nivel))
}

// ── Classificação ─────────────────────────────────────────────
export function classificarAcessibilidade(local) {
  const recursos = Object.values(local.acessibilidade || {})
  const total    = recursos.length
  const ativos   = recursos.filter(Boolean).length
  const pct      = total > 0 ? (ativos / total) * 100 : 0
  if (pct >= 80) return 'alto'
  if (pct >= 40) return 'medio'
  return 'baixo'
}

// ── Metadados de tipos ────────────────────────────────────────
export const TIPOS_META = {
  shopping:        { label: 'Shopping Center',      icone: 'ShoppingBag' },
  hospital:        { label: 'Hospital / UPA',       icone: 'Hospital' },
  educacao:        { label: 'Educação',             icone: 'GraduationCap' },
  espaco_publico:  { label: 'Praça / Parque',       icone: 'TreePine' },
  servico_publico: { label: 'Serviço Público',      icone: 'Building2' },
  banco:           { label: 'Agência Bancária',     icone: 'Landmark' },
  mercado:         { label: 'Mercado / Feira',      icone: 'Store' },
  cultura:         { label: 'Cultura e Lazer',      icone: 'Theater' },
  transporte:      { label: 'Terminal / Transporte',icone: 'BusFront' },
  supermercado:    { label: 'Supermercado',         icone: 'ShoppingCart' },
  esporte:         { label: 'Complexo Esportivo',   icone: 'Trophy' },
}

export const RECURSOS_META = {
  rampa:            { label: 'Rampa de acesso',    icone: 'Accessibility' },
  banheiroAdaptado: { label: 'Banheiro adaptado',  icone: 'Users' },
  vagaPCD:          { label: 'Vaga PCD',           icone: 'ParkingCircle' }, 
  elevador:         { label: 'Elevador',           icone: 'ArrowUpCircle' },
  entradaAcessivel: { label: 'Entrada acessível',  icone: 'DoorOpen' },
  calcadaAcessivel: { label: 'Calçada acessível',  icone: 'Footprints' },
}