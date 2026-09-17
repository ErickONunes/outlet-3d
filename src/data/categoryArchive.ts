import { articles, categories, categorySlug, photos } from './articles';
import migrated from './migrated.json';

export const POSTS_PER_PAGE = 12;

export type ArchiveCategory = { name: string; slug: string; url: string };

export const sourceCategories = Array.from(new Map(migrated.filter((item) => item.kind === 'post').flatMap((item) => item.categories).map((category: any) => [category.slug, category])).values()) as ArchiveCategory[];
const editorialCategories = categories.map((name) => ({ name, slug: categorySlug(name), url: `/categoria/${categorySlug(name)}/` }));
export const allCategories = [...editorialCategories.filter((editorial) => !sourceCategories.some((category) => category.name === editorial.name)), ...sourceCategories];

const summary = (text: string, limit = 140) => `${text.replace(/\s+/g, ' ').trim().slice(0, limit).replace(/\s+\S*$/, '')}…`;

export function getCategoryEntries(category: ArchiveCategory) {
  const selected = articles.filter((article) => article.category === category.name);
  const migratedPosts = migrated.filter((item) => item.kind === 'post' && item.categories.some((itemCategory: any) => itemCategory.slug === category.slug || itemCategory.name === category.name));
  return [...migratedPosts.map((item) => ({ path: item.path, title: item.title, description: summary(item.excerpt || item.seo.description), cover: item.cover, author: item.author, time: item.readingMinutes, category: category.name })), ...selected.map((item) => ({ path: `/artigos/${item.slug}/`, title: item.title, description: item.description, cover: { src: photos[item.image], alt: 'Impressora 3D em funcionamento', width: 800, height: 550 }, author: 'Erick Nunes', time: item.time, category: item.category }))].sort((a, b) => a.title.localeCompare(b.title, 'pt-BR'));
}

export const getPageCount = (total: number) => Math.max(1, Math.ceil(total / POSTS_PER_PAGE));
