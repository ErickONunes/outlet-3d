export type AffiliateMarketplace = 'mercado-livre' | 'amazon' | 'shopee';

export type AffiliateDraft = {
  marketplace: AffiliateMarketplace;
  affiliateUrl: string;
  productName: string;
  categorySlugs: string[];
  price?: number;
  previousPrice?: number;
  checkedAt: string;
  sourceSummary: string;
  editorialReason: string;
};

// Contrato para a futura automação por IA. A automação recebe uma URL do parceiro,
// extrai fatos verificáveis, sugere uma página e deixa a publicação para revisão humana.
export const affiliateWorkflow = {
  requiredFields: ['marketplace', 'affiliateUrl', 'productName', 'categorySlugs', 'checkedAt', 'sourceSummary', 'editorialReason'],
  allowedMarketplaces: ['mercado-livre', 'amazon', 'shopee'] as AffiliateMarketplace[],
  linkAttributes: 'sponsored noopener noreferrer',
  publicationRule: 'Não publicar preço, desconto, especificações ou recomendação sem revisão editorial e data de consulta.',
};
