---
version: 1
slug: "app-static-index-html"
primary_target: "app/static/index.html"
related_targets: ["app/static/styles.css","app/static/app.js"]
---

# Surface Brief — `app/static/index.html`

- **Scope & Mode:** Workspace operacional completo do `chat-pops` (`operate`, com disciplina de leitura clínica estruturada na folha de protocolo).
- **Audience & Job:** Enfermeiros, técnicos, residentes, internos e gestores da CCIH no HU-UFC consultando POPs homologados em segundos no plantão, conferindo materiais de bandeja, cadastrando/importando protocolos e monitorando lacunas de cobertura e protocolos mais acessados.
- **Constraints:** Zero PII/PHI (LGPD), 100% vinculado à tabela SQL `pops` (`status = 'ATIVO'`), dados iniciais de 5 POPs EBSERH/HU, lacunas e logs rotulados como `[DEMO]`, alvos de toque mínimos de `44px`, contraste WCAG AA `>= 4.5:1`, responsivo em Desktop (`> 1160px`), Tablet (`768px–1160px`) e Smartphone (`< 768px`).

## Direction contract

- **THESIS:** Traduz o fichário físico de POPs do posto de enfermagem para uma ferramenta digital cirúrgica — uma folha única leitosa de acetato montada sobre uma pilha escalonada de divisórias rígidas coloridas por comissão/função na borda direita — recusando o chat SaaS corporativo cinza ou azul genérico de bolhas flutuantes.
- **OWN-WORLD:** Folha leitosa contínua (`#F6F4EC` / `rgba(246, 244, 236, 0.95)`) com micro-textura fosca sobre prancha divisória saturada ativa (`#0D6B63` Enfermagem/Consulta, `#2F6B3B` Catálogo Vigente, `#1E4B94` Importar/Novo POP, `#A84311` CCIH/Lacunas), controles internos claros (`#FBF9F4`), tinta de impressão `#181B1A`, fios de `1px` (`#C7C2B4`), furos de encadernação com aro de tinta na margem esquerda, tarja vermelha vermelhão (`#B92525`) exclusiva para biossegurança/recusa segura, tipografia `Archivo` condensada (`wdth` `86%` em títulos e abas) + `Spectral` (leitura de etapas) + `JetBrains Mono` tabular, e chaveamento mecânico seco de `90ms steps(2)` combinado a um único assentamento inicial da folha.
- **STORY:** Ao abrir, o profissional vê de imediato o protocolo ativo homologado completo na primeira dobra, marca os itens físicos da bandeja com círculos perfurados, lê os passos e a tarja crítica da CCIH sem precisar rolar a janela, ou consulta um novo procedimento sabendo que qualquer ausência vira demanda auditada para a gestão.
- **FIRST VIEWPORT:** Em `1440×900`, o fichário cabe integralmente em `100vh` (`900px`): a prancha verde-petróleo (`#0D6B63`) e o cartão de suporte (`#DFDBC9`) sustentam a folha perfurada dividida em trilho de furos (`54px`), coluna de consulta e índice rápido à esquerda (`420px`, com `#form-chat` visível na base) e folha normativa à direita exibindo cabeçalho `POP.ENF.001`, grade bilateral de Bandeja Conferida + Passos de Execução e tarja vermelha de Biossegurança inteira acima da dobra, flanqueada pelas 4 abas verticais escalonadas contínuas na margem direita (`64px`). Em mobile (`< 768px`), adapta-se para barra superior da divisória ativa + faixa horizontal imediata de 4 abas (`>= 56px`), ocultando título duplicado e rolando suavemente até a folha de protocolo ao selecionar um POP.
- **FORM:** Challenger competitivo `rw-manual-acetate-tab-board` escolhido pelo usuário na Rodada 2 sobre lista fundamentada de 7 candidatos; `seed:2f81a577776fa2d2`.
- **FINISH:** unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
