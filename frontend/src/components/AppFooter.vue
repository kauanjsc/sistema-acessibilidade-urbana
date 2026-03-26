<template>
  <!--
    <footer> com role="contentinfo" é implícito no contexto do documento.
    Contém informações sobre a página como autor, copyright, etc. (WCAG 1.3.1).
  -->
  <footer class="app-footer" role="contentinfo">
    <div class="container app-footer__inner">

      <div class="app-footer__brand">
        <Accessibility aria-hidden="true" class="app-footer__icon" :size="32" />
        <div>
          <p class="app-footer__name">Teresina Acessível</p>
          <p class="app-footer__desc">
            Mapeamento urbano de acessibilidade — Teresina, Piauí
          </p>
        </div>
      </div>

      <div class="app-footer__info">
        <p>
          Trabalho de Conclusão de Curso — Ciência da Computação
        </p>
        <p>
        Aluno: Kauan Joaquim Santos Cardoso — Orientador: Prof. Dr. Mauricio Rego 
        </p>
        <p class="app-footer__wcag">
          <!-- Link para documentação de acessibilidade (WCAG 3.1.1 idioma declarado) -->
          Esta plataforma segue as diretrizes
          <a
            href="https://www.w3.org/WAI/WCAG21/Understanding/"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Diretrizes WCAG 2.1 — abre em nova janela"
          >
            WCAG 2.1
          </a>
          e padrões do
          <a
            href="https://www.gov.br/ds/"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Design System do Governo Federal — abre em nova janela"
          >
            Design System Gov.br
          </a>
        </p>
      </div>

    </div>

    <div class="app-footer__bottom">
      <div class="container">
        <p>© {{ currentYear }} — Dados simulados para fins acadêmicos. Teresina, PI.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { Accessibility } from 'lucide-vue-next'
const currentYear = new Date().getFullYear()
</script>

<style scoped>
.app-footer {
  background: var(--color-primary-darker);
  color: rgba(255,255,255,.85);
  margin-top: auto;
}
.app-footer__inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-8);
  padding: var(--space-10) var(--space-6);
  align-items: start;
}
.app-footer__brand {
  display: flex;
  gap: var(--space-3);
  align-items: flex-start;
}
.app-footer__icon {
  font-size: 2rem;
  flex-shrink: 0;
}
.app-footer__name {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  color: var(--color-white);
  margin-bottom: var(--space-1);
}
.app-footer__desc {
  font-size: var(--font-size-sm);
  margin-bottom: 0;
}
.app-footer__info {
  font-size: var(--font-size-sm);
}
.app-footer__info p {
  margin-bottom: var(--space-2);
}
.app-footer__wcag a {
  color: var(--color-warning);
  text-decoration: underline;
}
.app-footer__wcag a:hover {
  color: var(--color-white);
}
.app-footer__bottom {
  background: rgba(0,0,0,.2);
  padding: var(--space-3) var(--space-6);
  font-size: var(--font-size-xs);
  color: rgba(255,255,255,.6);
}
.app-footer__bottom p { margin: 0; }

@media (max-width: 640px) {
  .app-footer__inner {
    grid-template-columns: 1fr;
    gap: var(--space-6);
  }
}
</style>
