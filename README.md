# Outlet 3D

Portal editorial em português sobre impressão 3D, fabricação aditiva, prototipagem, materiais e criatividade. Desenvolvido com [Astro](https://astro.build/) para entregar páginas estáticas rápidas, indexáveis e fáceis de manter. O domínio previsto é [outlet3d.com.br](https://outlet3d.com.br/).

## O que está incluído

- Home editorial, categorias, artigos e páginas institucionais com identidade visual própria.
- Piloto de migração de 10 posts e 8 páginas do WordPress, nos endereços originais.
- Recomendações comerciais com preço, condições, transparência de afiliado e links externos seguros.
- Dados estruturados, canonical, sitemap, `robots.txt` e `llms.txt` para SEO e mecanismos de IA.
- Espaços prontos para AdSense, ativados somente com variáveis de ambiente válidas.
- Formulário visual de contato; o envio precisa ser conectado a um provedor antes da publicação.

## Começar localmente

Requer Node.js 20 ou superior.

```bash
npm install
npm run dev
```

Abra `http://localhost:4321`. Para gerar a versão de produção:

```bash
npm run build
npm run preview
```

## Estrutura

| Caminho | Responsabilidade |
| --- | --- |
| `src/pages/` | Rotas Astro e páginas estáticas |
| `src/data/` | Artigos, produtos e conteúdo migrado |
| `src/components/` | Componentes reutilizáveis de anúncios e produto |
| `src/layouts/Layout.astro` | SEO global, navegação, rodapé e AdSense condicional |
| `src/styles/` | Sistema visual e estilos por tipo de página |
| `public/branding/` | Logos da Outlet 3D |
| `migration/` | Inventário e validação do piloto WordPress |
| `docs/` | Operação, arquitetura, publicação e curadoria |

## Documentação

- [Arquitetura e conteúdo](docs/arquitetura.md)
- [Operação editorial e SEO](docs/operacao-editorial.md)
- [Curadoria de afiliados](docs/curadoria-afiliados.md)
- [Publicação e checklist](docs/publicacao.md)
- [Relatório de migração](migration/RELATORIO.md)
- [Resultado do piloto](migration/pilot/RESULTADO.md)

## Migração WordPress

O piloto preserva 18 URLs: 10 posts e 8 páginas públicas. O inventário identificou 459 artigos, 8 páginas, 165 URLs de cursos e 13 Web Stories. A migração completa não está incluída: cursos, Stories, tabelas, iframes, mídia e redirecionamentos precisam de uma fase própria de validação.

Para conferir o piloto após iniciar o servidor:

```bash
python3 migration/pilot/validate.py
python3 migration/pilot/http-check.py
```

## Monetização e privacidade

Não há identificador AdSense, script de rastreamento ou formulário de envio configurado no repositório. Antes da publicação, configure os dados reais, publique `ads.txt` fornecido pelo Google e revise as páginas de privacidade, cookies, transparência e termos com responsável jurídico.

Links de afiliado abrem em uma nova aba com `rel="sponsored noopener noreferrer"`. Preços são registros editoriais com data de consulta, não uma integração de preço em tempo real.

## Licença

Código e conteúdo reservados. Consulte o titular antes de reutilizar qualquer material deste repositório.
