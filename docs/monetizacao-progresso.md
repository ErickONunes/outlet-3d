# Monetização Outlet 3D — progresso e como continuar

Documento vivo. **Regra do projeto: toda ação de monetização, curadoria ou alteração relevante deve ser registrada aqui** (seção "Registro de sessões") no mesmo commit da mudança. Detalhes de política de afiliados ficam em [curadoria-afiliados.md](curadoria-afiliados.md); medição em [analytics.md](analytics.md).

## 1. Contexto e diagnóstico (20/11/2026)

- Site: https://outlet3d.com.br (Astro estático, repositório `ErickONunes/outlet-3d`, branch `main`, deploy automático após o push; leva cerca de 1 a 5 minutos).
- Conteúdo: 467 páginas migradas do WordPress (459 artigos, 8 páginas), 15 categorias, Web Stories. Cerca de 361 artigos estão em "Impressão 3D", muitos no padrão "Impressão 3D de peças para X: descubra…" (tráfego informativo e raso).
- Já existiam: AdSense (`ads.txt`, slots condicionais), GA4 (`G-26SJB3QB08`), página `/recomendados/` com 1 produto (Bambu Lab A1).
- Problema central: pouca oferta comercial (1 produto, 13 de 467 artigos com algum link) e nenhum dado de tráfego/conversão à mão. Sem acesso ao Search Console nem ao GA4 nesta fase.
- Decisão do dono: começar por **afiliados (Mercado Livre)**, depois AdSense/SEO.

Plano geral recomendado (ordem): 1) afiliados em escala, 2) reescrever artigos que já ranqueiam (precisa de export do Search Console), 3) otimizar AdSense, 4) produto digital próprio, 5) captura de e-mail, 6) serviços/B2B, 7) distribuição (Web Stories, Reels/Shorts, Pinterest).

## 2. O que foi feito (tudo publicado em `main`)

| Commit | Entrega |
| --- | --- |
| `e8ab96b` | Componente `ArticleProductBox` (caixa "Recomendado para este tema" nos artigos), campos `topics`/`marketplace` no catálogo, produtos Ender-3 V3 SE, Mars 5 Ultra e Sunlu S4 Pro |
| `6d64cff` | Layout compacto da caixa (estilos `:global` para o componente filho) |
| `ecf8a00` | Preço da Bambu A1 atualizado (R$ 3.961, consulta 20/11/2026) |
| `2e37b39` | Comparativo `/comparativos/impressoras-3d/` (Ender SE × Bambu A1 × Mars 5 Ultra) |
| `9e96d5d` | Filamentos PLA e PETG Masterprint |
| `972f67d` | Comparativo `/comparativos/pla-vs-petg/` (com FAQ e schema) |
| `95d14b8`, `30ec4d0` | Bambu A1 Mini, Neptune 4 Pro, kit de 47 ferramentas; estreitamento dos temas do kit |
| `c296acf` | Ender-3 V3 KE, Neptune 4 e comparativo `/comparativos/melhores-impressoras-3d-ate-3000/` |
| `635bd14` | Paquímetro e graxa; página `/kit-para-iniciantes/` |
| `5825dd9` | Evento GA4 `affiliate_click` |

## 3. Catálogo atual (`src/data/products.ts`) — 13 produtos

Todos são do Mercado Livre, links `meli.la` gerados na conta de afiliado **ERICKONUNES** (etiqueta `erickoliveiranunes`). Preços são fotografias de uma data e **mudam rápido**.

| Slug | Produto | Preço | Vendedor | Link | Consulta |
| --- | --- | --- | --- | --- | --- |
| `bambu-lab-a1-combo-ams-lite` | Bambu Lab A1 Combo AMS Lite | R$ 3.961 (ref. 5.300, 25%) | Berga Eletro | meli.la/1rvn5G8 | 20/11/2026 |
| `creality-ender-3-v3-se` | Creality Ender-3 V3 SE | R$ 1.181,28 no Pix (ref. 1.899) | RAIKOU | meli.la/32YxUwC | 20/11/2026 |
| `creality-ender-3-v3-ke` | Creality Ender-3 V3 KE | R$ 1.771,46 no Pix | Mega Mamute | meli.la/2KdFdcX | 20/11/2026 |
| `elegoo-neptune-4` | Elegoo Neptune 4 | R$ 2.369,99 (ref. 2.999, 20%) | STAR2GO (oficial) | meli.la/2Accsef | 20/11/2026 |
| `elegoo-neptune-4-pro` | Elegoo Neptune 4 Pro | R$ 2.540,43 | Processtec Desde 2003 Online | meli.la/31k4VwT | 20/11/2026 |
| `bambu-lab-a1-mini-combo-ams-lite` | Bambu Lab A1 Mini Combo | R$ 3.999,90 | Mega Byte (da listagem) | meli.la/1MAuodr | 20/11/2026 |
| `elegoo-mars-5-ultra` | Elegoo Mars 5 Ultra 9K (resina) | R$ 2.799 | Translaser | meli.la/1z2DScB | 20/11/2026 |
| `masterprint-pla-preto-1kg` | Filamento PLA Masterprint preto 1 kg | R$ 95,06 | MAGICLICK | meli.la/2tTsbcv | 20/11/2026 |
| `masterprint-petg-preto-1kg` | Filamento PETG Masterprint preto 1 kg | R$ 63,88 | FLY3DPARTSENGENHARIA | meli.la/2ZkZqv6 | 20/11/2026 |
| `sunlu-s4-pro-secador-filamento` | Sunlu S4 Pro (secador) | R$ 1.099 (ref. 1.373, 20%) | MegaPrint | meli.la/25yY7Zd | 20/11/2026 |
| `kit-47-ferramentas-impressao-3d` | Kit 47 ferramentas | R$ 76,53 | CHBFDCEGA15502 | meli.la/1vTBRbQ | 20/11/2026 |
| `paquimetro-digital-ocio-150mm` | Paquímetro digital Ócio 150 mm | R$ 26,99 | Ócio (oficial) | meli.la/28kPe4P | 21/11/2026 |
| `graxa-lubrificante-impressora-3d` | Graxa lubrificante | R$ 23,76 | FORGE_DREAMS_3D | meli.la/2RJ2QWp | 21/11/2026 |

**Renovar preços:** a cada ~2 semanas e antes de qualquer campanha. Itens mais voláteis: impressoras. Os dados de oferta são estáticos (não há monitoramento automático).

## 4. Páginas e componentes criados

- `src/components/ArticleProductBox.astro`: lista até 2 produtos cujo `topics` aparece no título do artigo (`productsForArticle` em `products.ts`). Sem correspondência, não renderiza nada. Inserido ao fim do conteúdo em `src/pages/[...path].astro`.
- `src/components/ProductOffer.astro`: preço, referência, desconto, parcelamento; novo campo `paymentNote` (ex.: "no Pix").
- Páginas: `/comparativos/impressoras-3d/`, `/comparativos/pla-vs-petg/`, `/comparativos/melhores-impressoras-3d-ate-3000/` (filtra por `offer.price <= 3000`), `/kit-para-iniciantes/` (soma calculada do catálogo). Estilos em `src/styles/comparison.css` e `starter-kit.css`. Todas aparecem em `/recomendados/` e no sitemap.
- Rastreamento: `Layout.astro` envia `affiliate_click` ao GA4 para links `rel~="sponsored"`, com `product_name`, `placement`, `page_path`, `link_url`.

### Temas (`topics`) e onde as caixas aparecem

A correspondência é por substring no título (minúsculas). Ao criar `topics`, teste no build para evitar caixas fora de contexto (ex.: o tema `ferramentas` foi removido por casar com "Ferramentas customizadas"). Contagem aproximada no último build: Ender SE ~30 páginas, Mars ~12, PETG ~7, kit de ferramentas ~11, PLA ~4, Neptune 4 Pro só na própria página.

## 5. Como cadastrar um produto novo (procedimento)

1. Abrir o Mercado Livre no Chrome do dono (logado; painel em `mercadolivre.com.br/afiliados/hub`). O navegador do app não tem a sessão; usar a extensão Claude in Chrome. Senhas nunca são digitadas pelo assistente.
2. Buscar o produto em `lista.mercadolivre.com.br/...`, abrir a página `…/p/MLB…` e anotar título, preço, vendedor e imagem (`og:image`).
3. Gerar o link em **Gerador de links** (`/afiliados/linkbuilder`): colar a URL do produto (várias, uma por linha) e clicar em Gerar; ler o `meli.la` dos campos.
4. Adicionar o item em `src/data/products.ts` (campos `affiliateUrl`, `offer`, `topics`, `marketplace:'Mercado Livre'`).
5. `npm run build`, conferir em preview (`npx astro preview --port 4399`), commitar e só então fazer push (o dono aprova cada push).
6. Atualizar este documento (tabela do catálogo e "Registro de sessões").

Regras de dados: não inventar preço anterior, desconto, estoque, avaliação ou teste; omitir `previousPrice` quando a referência parecer inflada ou duvidosa; informar `paymentNote` quando o preço for no Pix; deixar fora anúncios ambíguos (ex.: kit de bicos com "5 unidades" no título e "1 bico" na ficha). Textos devem dizer que não houve testes próprios.

## 6. Limites e pendências conhecidas

- Sem dados de tráfego/conversão. Em 20/11/2026 o painel do ML mostrava 0 cliques em 7 dias.
- **GA4 (dono):** criar dimensões personalizadas de evento `product_name` e `placement` (Administrador → Definições personalizadas) para ver produto e local nos relatórios.
- Páginas novas conferidas no desktop; apenas `/comparativos/pla-vs-petg/` foi testada no celular. Testar no celular: kit, comparativo de impressoras e o "até R$ 3.000".
- Cliques reais nos links `meli.la` não foram testados de ponta a ponta (curl recebe 403 por ser robô).
- Vendedores da Ender SE e da A1 Mini vieram da listagem de busca, não da página do produto.
- Formulário de contato ainda não está conectado a um provedor de envio.
- Teste do evento no site real em 21/11/2026 pode ter gerado 1 `affiliate_click` de teste (PETG, `/comparativos/pla-vs-petg/`).
- Só o programa do Mercado Livre foi usado. Amazon e Shopee ainda não.

## 7. Próximos passos sugeridos

1. Esperar 1 a 2 semanas e ler `affiliate_click` no GA4 + métricas do painel do ML.
2. Search Console: exportar páginas com mais impressões; escolher 20 a 30 artigos para reescrever (comparativo, tabela, caixa de produto, títulos sem "Descubra…").
3. Captura de e-mail com lead magnet (checklist de calibração / guia do primeiro mês) e conexão do formulário de contato.
4. Rotina de renovação de preços (a cada 2 semanas).
5. Avaliar Amazon/Shopee; mais acessórios só se os dados pedirem.
6. Depois: otimizar AdSense (testar Auto Ads, revisar consentimento), produto digital próprio, patrocínios/serviços.

## 8. Registro de sessões

Formato: data — o que foi feito — commits — pendências geradas. Acrescentar uma linha a cada sessão.

- **2026-11-20/21** — Análise do site e plano de monetização; infraestrutura de caixas de produto; 13 produtos do Mercado Livre com links de afiliado e preços conferidos; 3 comparativos e o kit para iniciantes; rastreamento `affiliate_click` no GA4; verificação no ar de caixas, comparativos, kit e rastreamento. Commits `e8ab96b` a `5825dd9`. Pendências: dimensões no GA4, teste em celular, dados do Search Console.
