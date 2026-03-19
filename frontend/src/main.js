/**
 * main.js — Ponto de entrada da aplicação Teresina Acessível
 */

import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'

// Design System Gov.br — tokens e utilitários globais
import './assets/govbr.css'
// Estilos globais dos modos de acessibilidade
import './assets/accessibility-modes.css'

const app = createApp(App)

app.use(router)

app.mount('#app')