# Arquitetura e conteúdo

## Princípios

O site é estático. O Astro transforma dados e componentes em HTML no build; não há banco de dados, painel administrativo ou API de produção. Isso favorece desempenho, segurança e custos de hospedagem baixos. A contrapartida é que cada atualização editorial precisa de uma alteração no repositório e novo deploy.

## Rotas

| Área | Origem | Exemplo |
| --- | --- | --- |
| Home | `src/pages/index.astro` | `/` |
| Artigos novos | `src/pages/artigos/[slug].astro` + `src/data/articles.ts` | `/artigos/primeira-impressao-3d/` |
| Categorias | `src/pages/categoria/[slug].astro` | `/categoria/guias-tutoriais/` |
| Conteúdo migrado | `src/pages/[...path].astro` + `src/data/migrated.json` | `/impressao-3d/.../` |
| Institucionais | conteúdo migrado ou `src/pages/[page].astro` | `/sobre/`, `/contato/` |
| Recomendações | `src/pages/recomendados/` + `src/data/products.ts` | `/recomendados/` |

## Dados

`articles.ts` contém conteúdos editoriais criados no projeto. `migrated.json` preserva os dados do piloto WordPress, incluindo caminho, data, SEO e HTML. Não edite o HTML migrado sem revisar a página correspondente.

`products.ts` é a fonte de verdade para a vitrine comercial. Cada produto possui nome, imagem, resumo, benefícios, público, URL de afiliado e, opcionalmente, uma oferta registrada. `ProductOffer.astro` exibe preço, desconto, economia, parcelamento e data de consulta de maneira consistente.

## SEO e descoberta por IA

`Layout.astro` gera title, description, canonical, Open Graph e grafo Organization/WebSite. Rotas de artigo e categoria acrescentam Schema.org contextual. O sitemap é gerado por `@astrojs/sitemap`; `robots.txt` aponta para ele. `public/llms.txt` apresenta aos agentes de IA a identidade editorial e as principais áreas do portal.

Não existem garantias de posição em busca ou de citação por ferramentas de IA. Qualidade factual, autoria identificada, atualidade, fontes e páginas úteis são os sinais que o projeto sustenta tecnicamente.
