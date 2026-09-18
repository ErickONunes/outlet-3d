# Plano de medição — Outlet 3D

## Implementação

- Ferramenta: Google Analytics 4 (GA4)
- Fluxo: `outlet3d` (`G-26SJB3QB08`)
- Coleta: `page_view` em todas as páginas estáticas, com a Medição otimizada do GA4 habilitada.
- Privacidade: nenhum dado pessoal é enviado pelo código do site. Não inclua e-mail, telefone, nome ou identificadores de contato em parâmetros de eventos.

## Eventos usados para decisões

| Evento | Origem | Decisão apoiada |
| --- | --- | --- |
| `page_view` | GA4 | Pautas e páginas que atraem descoberta orgânica. |
| `scroll` | Medição otimizada | Profundidade de leitura e qualidade dos artigos. |
| `click` de saída | Medição otimizada | Interesse em links de afiliados e parceiros. |
| `file_download` | Medição otimizada | Interesse em materiais para download. |

## Rotina de análise

1. Acompanhe aquisição orgânica, páginas de entrada e engajamento semanalmente.
2. Compare páginas de recomendação com cliques de saída antes de trocar ofertas afiliadas.
3. Marque uma conversão apenas quando houver um evento de negócio confiável, como envio confirmado de formulário ou clique de afiliado identificado.
4. Use UTMs em campanhas: `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` e `utm_term`, sempre em minúsculas.
