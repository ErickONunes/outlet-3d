# Importação completa — Outlet 3D

Data da importação: 17/09/2026.

## Resultado

| Item | Quantidade |
| --- | ---: |
| Posts públicos | 459 |
| Páginas públicas | 8 |
| Caminhos preservados | 467 |
| Categorias | 15 |
| Imagens locais referenciadas | 518 |
| Rotas geradas no build | 496 |

O importador usa as fotografias públicas exportadas pelo inventário WordPress em `migration/posts.json`, `pages.json`, `media.json`, `categories.json` e `users.json`. Ele sanitiza HTML, preserva estrutura editorial útil, copia imagens de `wp-content/uploads` e converte links internos de posts, páginas e categorias para rotas locais.

## SEO e GEO aplicados

- URL canônica original preservada em cada post e página.
- Title e meta description por documento, gerados a partir de título e resumo quando o WordPress não fornecia metadados públicos.
- `BlogPosting` com autor, publicação, atualização, categoria, contagem de palavras e acesso livre.
- `FAQPage` nas páginas cujo conteúdo contém um bloco FAQ estruturado.
- `CollectionPage` e `ItemList` para cada categoria.
- Organization e WebSite globais, sitemap, `robots.txt` permitindo robôs de busca/IA e `llms.txt` atualizado.
- Relações de leitura recomendada entre posts da mesma categoria.

## Limites e acompanhamento

Esta etapa preserva o acervo; ela não reescreve individualmente os 459 textos nem valida alegações históricas presentes na fonte. Páginas sobre produtos, normas, preços, saúde, segurança ou versões de software devem ser revisadas editorialmente antes de campanhas ou atualização de domínio.

Uma imagem da origem retornou 404 durante a cópia: `2024/10/impressao-3d-1024x585.jpg`. O post correspondente foi mantido e o elemento de imagem indisponível foi removido para evitar erro visual. O detalhe fica em `migration/import-all-manifest.json`.

Cursos e Web Stories encontrados somente no sitemap não foram importados porque faltam conteúdo e metadados verificáveis no inventário local.

## Repetir e validar

```bash
python3 migration/import-all.py
npm run build
python3 migration/validate-all.py
```

O importador não altera o site WordPress de origem.
