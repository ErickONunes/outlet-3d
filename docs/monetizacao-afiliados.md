# Monetização editorial e afiliados

## AdSense

Os artigos já chamam `AdSlot.astro`. Para habilitar a exibição, defina no ambiente de publicação:

```bash
PUBLIC_ADSENSE_ENABLED=true
PUBLIC_ADSENSE_CLIENT=ca-pub-SEU_ID
PUBLIC_ADSENSE_ARTICLE_SLOT=SEU_SLOT_NUMERICO
```

O componente não renderiza anúncios se os dados não forem válidos. Antes de publicar, cadastre o `ads.txt` fornecido pela conta AdSense, configure consentimento aplicável e revise a Política de Privacidade.

## Links de afiliado

O catálogo em `src/data/products.ts` já cria páginas de recomendação, preços consultados, avisos de transparência e links externos em nova aba com `rel="sponsored noopener noreferrer"`.

Para a automação futura, use o contrato em `src/data/affiliate.ts`. A IA deve receber uma URL de Mercado Livre, Amazon ou Shopee e devolver os campos de `AffiliateDraft`. A publicação continua dependente de revisão editorial, principalmente para preço, desconto, disponibilidade, imagens, afirmações técnicas e adequação ao artigo.

Cada recomendação deve informar que pode gerar comissão e apontar para `/transparencia/`. Não use links de afiliado em texto editorial sem identificação clara.

## Links internos nos artigos

Cada artigo agora apresenta anterior, próximo e conteúdos da mesma categoria. Isso cria caminhos de descoberta para leitores e facilita o rastreamento de tópicos pelos mecanismos de busca. Mantenha títulos de links descritivos; nunca use links genéricos como “clique aqui”.
