# Operação editorial e SEO

## Publicar um artigo novo

1. Adicione o item em `src/data/articles.ts` com slug único, categoria, descrição, tempo de leitura, imagem e seções.
2. Escreva título e descrição específicos; a descrição deve explicar o que a pessoa aprende ou resolve.
3. Use uma imagem com licença adequada e texto alternativo que descreva o conteúdo visual.
4. Execute `npm run build` e confira a rota, a categoria, a versão mobile e os links internos.
5. Ao publicar, revise o sitemap e solicite rastreamento no Search Console, quando a propriedade estiver configurada.

## Padrão de qualidade

- Diferencie fatos, opinião e recomendação comercial.
- Cite fontes primárias quando houver especificações, compatibilidade, segurança ou números importantes.
- Informe limites e condições de uso, especialmente em materiais, máquinas e peças funcionais.
- Atualize conteúdo que dependa de versões de software, preços, normas ou produtos.
- Evite gerar páginas semelhantes apenas para aumentar volume; cada URL deve responder a uma intenção clara.

## Checklist de SEO e GEO

- Um único `h1` que corresponda à intenção da busca.
- Introdução que responda à pergunta principal logo no início.
- Subtítulos descritivos, exemplos e termos técnicos explicados em contexto.
- Autor, data e atualização visíveis quando aplicável.
- Links para conteúdos relacionados e para fontes confiáveis.
- Imagem, canonical e dados estruturados coerentes com o texto.
- Sem promessas de resultado, citações sem fonte ou números não verificáveis.

## Conteúdo migrado

Conserve o caminho original, a data e as referências quando for necessário preservar tráfego. Antes de ajustar redação, faça uma cópia do conteúdo original e valide a rota. Para novas ondas de migração, inclua amostras de tabelas, iframes, vídeos e anexos antes de automatizar o restante.

## Publicidade

O componente `AdSlot.astro` só renderiza anúncios quando `PUBLIC_ADSENSE_ENABLED=true`, o cliente AdSense tem formato válido e existe slot configurado. A aprovação, consentimento, `ads.txt` e a conformidade de privacidade dependem da conta e da operação real; não habilite com valores de exemplo.
