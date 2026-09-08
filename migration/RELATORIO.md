# Inventário de migração — Outlet 3D

Consulta pública em 08/09/2026. Nenhum conteúdo do site de produção foi alterado.

| Item | Quantidade |
|---|---:|
| Artigos publicados (API e sitemap) | 459 |
| Páginas publicadas (API) | 8 |
| URLs de cursos no sitemap, sem arquivo de listagem | 165 |
| URLs de Web Stories, sem os dois arquivos de listagem | 13 |
| Categorias | 15 |
| Tags | 255 |
| Autores públicos | 2 |
| Mídias na biblioteca pública | 949 imagens |
| Comentários públicos | 0 |

São 645 itens de conteúdo identificados entre API e sitemaps. Cursos e Stories foram identificados pelas URLs; o conteúdo completo deles ainda não foi exportado/validado. Os sitemaps reúnem 649 URLs únicas incluindo início e arquivos. O sitemap de vídeo aponta a artigos já contados.

## Imagens e formatação

- 457 artigos possuem imagem destacada; 455 IDs de imagens destacadas distintos.
- 155 ocorrências de imagens no corpo dos artigos (não necessariamente arquivos únicos).
- Biblioteca: 671 JPEG, 246 WebP e 32 PNG.
- Tamanhos de originais disponíveis para 947/949 mídias somam 212.631.399 bytes, cerca de 213 MB decimais. Miniaturas/variantes e dois tamanhos desconhecidos não entram nesse total. Arquivos binários ainda não foram baixados.
- 105 artigos contêm tabelas; 12 contêm iframes; 5 contêm script, vídeo ou áudio. Grupos podem se sobrepor.
- Cerca de 789 mil palavras no HTML dos artigos após remoção simples das tags; é estimativa, não contagem editorial revisada.

## Migração proposta

1. Importar automaticamente o núcleo de 459 artigos e 8 páginas, com categorias, tags, autoria e datas.
2. Preservar URLs atuais (ex.: /impressao-3d/slug/) ou mapear cada mudança com redirecionamento 301. A prévia usa /artigos/slug/ e não deve substituir as URLs antigas sem adaptação.
3. Copiar e otimizar imagens; ajustar links internos e testar tabelas, iframes e conteúdo incorporado.
4. Avaliar separadamente 165 cursos e 13 Stories. Existem títulos de cursos fora do tema central; não excluir nem migrar automaticamente sem análise de relevância e tráfego.
5. Recolher títulos SEO, descrições, canonical e schema das páginas ou da exportação do Rank Math; esses campos não aparecem no JSON público dos posts.
6. Reconfigurar anúncios, medição e consentimento conforme a configuração real do cliente.

## Limites

API pública não inclui necessariamente rascunhos, conteúdo privado, usuários sem publicações, configurações de plugins ou redirecionamentos. Sitemap não prova indexação no Google nem tráfego. Para fechar escopo e priorização: backup/exportação do WordPress e acesso de leitura a Search Console/Analytics.

## Arquivos

- url-inventory.csv: 467 artigos e páginas, com título, URL, datas e indicadores de conteúdo.
- all-sitemap-urls.csv: URLs únicas de todos os sitemaps.
- posts.json, pages.json, categories.json, tags.json, users.json e media.json: fotografia dos dados públicos (não é backup completo).
- sitemap-inventory.json e summary.json: contagens e inventário técnico.
