# Outlet 3D — Astro

Portal editorial estático em português. Execute `npm install` e `npm run dev`. A produção é gerada em `dist/` com `npm run build`.

## Conteúdo

Artigos introdutórios em `src/data/articles.ts`. Categorias e páginas são geradas estaticamente. Esta primeira versão contém cinco textos novos; não migra o acervo do WordPress. Antes de substituir o domínio atual, exporte o conteúdo existente, preserve os slugs ou configure redirecionamentos 301 e revise os textos.

## Monetização

Nenhum script AdSense foi ativado e nenhum publisher ID foi inventado. A ativação depende da conta e aprovação do cliente. Depois de configurar a conta, inserir o código oficial, identificar os espaços publicitários, publicar o ads.txt fornecido pelo Google e revisar privacidade/consentimento conforme o funcionamento real. Não há garantia de aprovação ou receita.

## Imagens

Fotos de Jakub Żerdzicki no Unsplash, carregadas externamente:
- https://unsplash.com/photos/3d-printer-creating-a-red-object-with-yellow-filament-W_SYA5yU9p8
- https://unsplash.com/photos/a-close-up-of-a-3d-printer-machine-FED1QYdR1qI

## Antes da publicação no domínio

Revisar os artigos, informações do autor e páginas institucionais com o cliente; migrar URLs e conteúdo; escolher hospedagem estática e configurar DNS. As referências canônicas e o sitemap usam https://outlet3d.com.br.

## Piloto de migração — 08/09/2026

Importados os 10 posts mais recentes do inventário e as 8 páginas públicas. Dados publicados em `src/data/migrated.json`; rotas originais geradas por `src/pages/[...path].astro`; imagens mantidas em `public/wp-content/uploads/` com os mesmos caminhos. Os cinco artigos da versão inicial continuam disponíveis, mas não entram na contagem da migração.

- `migration/pilot/manifest.json`: IDs, URLs, imagens e ajustes documentados.
- `migration/pilot/source/`: fotografia dos 18 conteúdos de origem para comparação.
- `python3 migration/pilot/validate.py`: valida o build contra essa fotografia.
- `python3 migration/pilot/http-check.py`: valida as rotas e imagens com o servidor local em localhost:4321.
- `migration/pilot/import.py`: importação limitada e repetível; exige os JSONs do inventário local, obtidos com `migration/audit.py`. Não amplia a seleção automaticamente.

Textos e metadados foram preservados, com uma adaptação documentada no contato: substituição do shortcode quebrado pelo e-mail. Home e Cookies já estavam vazios na origem; os caminhos foram preservados com links úteis, sem inventar uma política. As informações institucionais continuam sendo as do site original e precisam de revisão antes da troca definitiva do domínio. Links para conteúdo fora do piloto continuam absolutos no site atual.

O piloto cobre texto, imagem destacada, dados estruturados e páginas institucionais. Os 10 artigos selecionados não têm tabelas ou iframes; esses formatos precisam entrar numa próxima amostra antes da migração completa. A conta AdSense e o domínio de produção não foram alterados.
