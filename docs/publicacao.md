# Publicação e checklist

## Hospedagem estática

O diretório `dist/`, criado por `npm run build`, pode ser publicado em Cloudflare Pages, Netlify, Vercel, GitHub Pages com adaptador adequado ou outro host estático. Configure:

- comando de build: `npm run build`;
- diretório de publicação: `dist`;
- Node.js 20 ou superior;
- domínio: `outlet3d.com.br` e `www.outlet3d.com.br`, conforme a estratégia de DNS;
- redirecionamento HTTPS e uma única versão canônica do domínio.

## Variáveis de ambiente

| Variável | Uso | Obrigatória? |
| --- | --- | --- |
| `PUBLIC_ADSENSE_ENABLED` | Ativa anúncios somente com valor `true` | Não |
| `PUBLIC_ADSENSE_CLIENT` | ID `ca-pub-...` real da conta Google | Não |
| `PUBLIC_ADSENSE_ARTICLE_SLOT` | Slot real em páginas de artigo | Não |

Não inclua chaves privadas, senhas ou tokens em arquivos `PUBLIC_*`: esses valores podem ser entregues ao navegador.

## Antes de apontar o domínio

1. Execute `npm run build` sem erros.
2. Teste home, artigos, categorias, páginas institucionais e recomendações em desktop e celular.
3. Valide as 5 Web Stories do piloto, os artigos, as categorias e confirme que não existem links quebrados.
4. Configure redirecionamentos 301 para qualquer URL que mudar. Não substitua URLs antigas por páginas genéricas.
5. Revise autor, contato, privacidade, cookies, termos, transparência, imagens e direitos de uso.
6. Configure Search Console, Analytics e AdSense somente com IDs do cliente e consentimento aplicável.
7. Verifique sitemap, `robots.txt`, canonical e `llms.txt` no domínio final.
8. Faça uma cópia de segurança do WordPress antes de qualquer migração completa.

## Após publicar

Monitore respostas 404, cobertura do Search Console, desempenho das páginas e mudanças de preço dos produtos recomendados. Atualize a oferta editorial antes de reutilizá-la em campanhas ou anúncios.
